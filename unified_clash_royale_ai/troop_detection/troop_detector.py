import cv2
import numpy as np
import json
import os
import sys
from ultralytics import YOLO
from ultralytics .engine .results import Results
sys .path .insert (0 ,os .path .dirname (os .path .dirname (os .path .abspath (__file__ ))))
from unified_clash_royale_ai .config import YOLO_MODEL
class TroopDetector :
    def __init__ (self ,model_path =None ,confidence_threshold =0.4 ):
        self .model_path =model_path or YOLO_MODEL
        self .confidence_threshold =confidence_threshold
        try :
            if model_path and os .path .exists (model_path ):
                self .model =YOLO (model_path )
            else :
                self .model =YOLO ("yolov8n.pt")
                print ("Предупреждение: используется модель YOLO по умолчанию. Пожалуйста, предоставьте обученную модель.")
        except Exception as e :
            print (f"Error loading YOLO model: {e }")
            self .model =None
    def detect_troops (self ,screenshot ):
        if self .model is None :
            return []
        try :
            results =self .model .predict (
            source =screenshot ,
            stream =True ,
            conf =self .confidence_threshold ,
            verbose =False
            )
            detections =[]
            for result in results :
                results_json =result .tojson ()
                try :
                    results_data =json .loads (results_json )
                except json .JSONDecodeError :
                    print ("Ошибка декодирования JSON из результатов YOLO")
                    return []
                for item in results_data :
                    box =item .get ('box')
                    if not box :
                        continue
                    try :
                        center_x =(box ['x1']+box ['x2'])/2
                        center_y =(box ['y1']+box ['y2'])/2
                        name =item .get ('name','unknown')
                        detections .append ((name ,(center_x ,center_y )))
                    except (KeyError ,TypeError )as e :
                        print (f"Error processing box data: {box }, Error: {e }")
                        continue
            return detections ,result
        except Exception as e :
            print (f"Error in troop detection: {e }")
            return [],None
    def categorize_troops (self ,detections ,screen_height ):
        troops ={
        "left":([],[]),
        "right":([],[]),
        "all":([],[])
        }
        ally_troops ={
        "left":([],[]),
        "right":([],[]),
        "all":([],[])
        }
        middle_y =screen_height /2
        for troop_name ,(x ,y )in detections :
            if troop_name .startswith ("enemy_"):
                if y <=middle_y :
                    troops ["left"][0 ].append (troop_name )
                    troops ["left"][1 ].append ((x ,y ))
                else :
                    troops ["right"][0 ].append (troop_name )
                    troops ["right"][1 ].append ((x ,y ))
                troops ["all"][0 ].append (troop_name )
                troops ["all"][1 ].append ((x ,y ))
            elif troop_name .startswith ("ally_"):
                if y <=middle_y :
                    ally_troops ["left"][0 ].append (troop_name )
                    ally_troops ["left"][1 ].append ((x ,y ))
                else :
                    ally_troops ["right"][0 ].append (troop_name )
                    ally_troops ["right"][1 ].append ((x ,y ))
                ally_troops ["all"][0 ].append (troop_name )
                ally_troops ["all"][1 ].append ((x ,y ))
        return troops ,ally_troops
    def find_optimal_center (self ,coordinates ,radius ):
        max_count =0
        max_center =None
        for potential_center in coordinates :
            count =0
            for other_point in coordinates :
                distance =np .sqrt (
                (potential_center [0 ]-other_point [0 ])**2 +
                (potential_center [1 ]-other_point [1 ])**2
                )
                if distance <=radius :
                    count +=1
            if count >max_count :
                max_count =count
                max_center =potential_center
        return max_center ,max_count