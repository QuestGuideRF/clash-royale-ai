import os
import cv2
import json
import time
import numpy as np
from datetime import datetime
import threading
from queue import Queue
class DataCollector :
    def __init__ (self ,output_dir ="training_data"):
        self .output_dir =output_dir
        self .is_collecting =False
        self .data_queue =Queue ()
        self .collection_thread =None
        self .cards_dir =os .path .join (output_dir ,'cards')
        self .yolo_dir =os .path .join (output_dir ,'yolo')
        self .rl_dir =os .path .join (output_dir ,'rl')
        for dir_path in [self .cards_dir ,self .yolo_dir ,self .rl_dir ]:
            os .makedirs (dir_path ,exist_ok =True )
    def start_collection (self ,screen_capture ,mode ='all'):
        self .is_collecting =True
        self .screen_capture =screen_capture
        self .mode =mode
        self .collection_thread =threading .Thread (target =self ._collection_loop )
        self .collection_thread .start ()
        print (f"Сбор данных начат в режиме: {mode }")
    def stop_collection (self ):
        self .is_collecting =False
        if self .collection_thread :
            self .collection_thread .join ()
        print ("Сбор данных остановлен")
    def _collection_loop (self ):
        frame_count =0
        while self .is_collecting :
            try :
                screenshot =self .screen_capture .take_screenshot ()
                timestamp =datetime .now ().strftime ("%Y%m%d_%H%M%S_%f")
                if self .mode in ['cards','all']:
                    self ._collect_card_data (screenshot ,timestamp )
                if self .mode in ['yolo','all']:
                    self ._collect_yolo_data (screenshot ,timestamp ,frame_count )
                if self .mode in ['rl','all']:
                    self ._collect_rl_data (screenshot ,timestamp )
                frame_count +=1
                time .sleep (0.5 )
            except Exception as e :
                print (f"Ошибка сбора данных: {e }")
                time .sleep (1 )
    def _collect_card_data (self ,screenshot ,timestamp ):
        card_regions =[
        (125 ,848 ,221 ,971 ),
        (229 ,848 ,325 ,971 ),
        (333 ,848 ,429 ,971 ),
        (437 ,848 ,533 ,971 ),
        ]
        for i ,(x1 ,y1 ,x2 ,y2 )in enumerate (card_regions ):
            if y2 <=screenshot .shape [0 ]and x2 <=screenshot .shape [1 ]:
                card_img =screenshot [y1 :y2 ,x1 :x2 ]
                card_img =cv2 .resize (card_img ,(32 ,32 ))
                unlabeled_dir =os .path .join (self .cards_dir ,'unlabeled')
                os .makedirs (unlabeled_dir ,exist_ok =True )
                cv2 .imwrite (
                os .path .join (unlabeled_dir ,f'card_{timestamp }_{i }.png'),
                card_img
                )
    def _collect_yolo_data (self ,screenshot ,timestamp ,frame_count ):
        images_dir =os .path .join (self .yolo_dir ,'images','unlabeled')
        os .makedirs (images_dir ,exist_ok =True )
        img_path =os .path .join (images_dir ,f'frame_{timestamp }.png')
        cv2 .imwrite (img_path ,screenshot )
        labels_dir =os .path .join (self .yolo_dir ,'labels','unlabeled')
        os .makedirs (labels_dir ,exist_ok =True )
        label_path =os .path .join (labels_dir ,f'frame_{timestamp }.txt')
        open (label_path ,'w').close ()
    def _collect_rl_data (self ,screenshot ,timestamp ):
        state_dir =os .path .join (self .rl_dir ,'states')
        os .makedirs (state_dir ,exist_ok =True )
        processed =cv2 .resize (screenshot ,(160 ,208 ))
        processed =cv2 .cvtColor (processed ,cv2 .COLOR_BGR2GRAY )
        np .save (
        os .path .join (state_dir ,f'state_{timestamp }.npy'),
        processed
        )
    def label_card_data (self ,card_name ,image_paths ):
        card_dir =os .path .join (self .cards_dir ,card_name )
        os .makedirs (card_dir ,exist_ok =True )
        for path in image_paths :
            if os .path .exists (path ):
                filename =os .path .basename (path )
                new_path =os .path .join (card_dir ,filename )
                os .rename (path ,new_path )
    def create_yolo_annotation (self ,image_path ,annotations ):
        label_path =image_path .replace ('/images/','/labels/').replace ('.png','.txt').replace ('.jpg','.txt')
        with open (label_path ,'w')as f :
            for ann in annotations :
                class_id ,x_center ,y_center ,width ,height =ann
                f .write (f"{class_id } {x_center } {y_center } {width } {height }\n")
    def get_statistics (self ):
        stats ={
        'cards':{'total':0 ,'by_class':{}},
        'yolo':{'total':0 ,'labeled':0 ,'unlabeled':0 },
        'rl':{'total':0 }
        }
        for class_name in os .listdir (self .cards_dir ):
            class_path =os .path .join (self .cards_dir ,class_name )
            if os .path .isdir (class_path ):
                count =len ([f for f in os .listdir (class_path )if f .endswith ('.png')])
                stats ['cards']['by_class'][class_name ]=count
                stats ['cards']['total']+=count
        images_dir =os .path .join (self .yolo_dir ,'images')
        if os .path .exists (images_dir ):
            for subset in ['train','val','unlabeled']:
                subset_dir =os .path .join (images_dir ,subset )
                if os .path .exists (subset_dir ):
                    count =len ([f for f in os .listdir (subset_dir )if f .endswith (('.png','.jpg'))])
                    if subset =='unlabeled':
                        stats ['yolo']['unlabeled']=count
                    else :
                        stats ['yolo']['labeled']+=count
                    stats ['yolo']['total']+=count
        states_dir =os .path .join (self .rl_dir ,'states')
        if os .path .exists (states_dir ):
            stats ['rl']['total']=len ([f for f in os .listdir (states_dir )if f .endswith ('.npy')])
        return stats