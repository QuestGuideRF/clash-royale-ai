import os
import yaml
import shutil
from datetime import datetime
try :
    from ultralytics import YOLO
    HAS_YOLO =True
except ImportError :
    HAS_YOLO =False
class YOLOTrainer :
    def __init__ (self ,data_dir ="training_data/yolo",model_dir ="models/yolo"):
        self .data_dir =data_dir
        self .model_dir =model_dir
        self .model =None
        os .makedirs (model_dir ,exist_ok =True )
        os .makedirs (os .path .join (data_dir ,'images','train'),exist_ok =True )
        os .makedirs (os .path .join (data_dir ,'images','val'),exist_ok =True )
        os .makedirs (os .path .join (data_dir ,'labels','train'),exist_ok =True )
        os .makedirs (os .path .join (data_dir ,'labels','val'),exist_ok =True )
    def create_dataset_yaml (self ,classes ):
        dataset_config ={
        'path':os .path .abspath (self .data_dir ),
        'train':'images/train',
        'val':'images/val',
        'names':{i :name for i ,name in enumerate (classes )}
        }
        yaml_path =os .path .join (self .data_dir ,'dataset.yaml')
        with open (yaml_path ,'w')as f :
            yaml .dump (dataset_config ,f )
        return yaml_path
    def load_pretrained (self ,model_name ='yolov8n.pt'):
        if not HAS_YOLO :
            raise ImportError ("ultralytics не установлен")
        self .model =YOLO (model_name )
        return self .model
    def train (self ,epochs =100 ,imgsz =640 ,batch =16 ,device ='0'):
        if self .model is None :
            self .load_pretrained ()
        yaml_path =os .path .join (self .data_dir ,'dataset.yaml')
        if not os .path .exists (yaml_path ):
            raise FileNotFoundError ("Создайте dataset.yaml с помощью create_dataset_yaml()")
        timestamp =datetime .now ().strftime ("%Y%m%d_%H%M%S")
        results =self .model .train (
        data =yaml_path ,
        epochs =epochs ,
        imgsz =imgsz ,
        batch =batch ,
        device =device ,
        project =self .model_dir ,
        name =f'train_{timestamp }',
        patience =20 ,
        save =True ,
        plots =True
        )
        return results
    def validate (self ):
        if self .model is None :
            raise ValueError ("Модель не загружена")
        yaml_path =os .path .join (self .data_dir ,'dataset.yaml')
        results =self .model .val (data =yaml_path )
        return results
    def export (self ,format ='onnx'):
        if self .model is None :
            raise ValueError ("Модель не загружена")
        return self .model .export (format =format )
    def fine_tune (self ,pretrained_path ,epochs =50 ):
        self .model =YOLO (pretrained_path )
        return self .train (epochs =epochs )
    @staticmethod
    def get_clash_royale_classes ():
        return [
        'ally_knight','ally_archers','ally_giant','ally_prince',
        'ally_mini_pekka','ally_musketeer','ally_valkyrie','ally_hog_rider',
        'ally_wizard','ally_witch','ally_golem','ally_pekka',
        'ally_balloon','ally_minions','ally_skeleton_army','ally_goblin',
        'ally_goblin_barrel','ally_electro_wizard','ally_mega_knight',
        'enemy_knight','enemy_archers','enemy_giant','enemy_prince',
        'enemy_mini_pekka','enemy_musketeer','enemy_valkyrie','enemy_hog_rider',
        'enemy_wizard','enemy_witch','enemy_golem','enemy_pekka',
        'enemy_balloon','enemy_minions','enemy_skeleton_army','enemy_goblin',
        'enemy_goblin_barrel','enemy_electro_wizard','enemy_mega_knight',
        'cannon','tesla','inferno_tower','bomb_tower','goblin_hut',
        'ally_princess_tower','ally_king_tower',
        'enemy_princess_tower','enemy_king_tower'
        ]