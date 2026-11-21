import cv2
import numpy as np
from keras .models import load_model
from keras .preprocessing .image import img_to_array
import os
from imutils import paths
import os
import sys
sys .path .insert (0 ,os .path .dirname (os .path .dirname (os .path .abspath (__file__ ))))
from unified_clash_royale_ai .config import CARD_RECOGNITION_MODEL ,CARD_PLACEMENT_MODEL
class CardDetector :
    def __init__ (self ,model_path1 =None ,model_path2 =None ,card_collection_path =None ):
        self .model_path1 =model_path1 or CARD_RECOGNITION_MODEL
        self .model_path2 =model_path2 or CARD_PLACEMENT_MODEL
        self .card_collection_path =card_collection_path or "cardCollection.txt"
        if os .path .exists (self .model_path1 ):
            self .model1 =load_model (self .model_path1 )
        else :
            print (f"Warning: Model {self .model_path1 } not found")
            self .model1 =None
        if os .path .exists (self .model_path2 ):
            self .model2 =load_model (self .model_path2 )
        else :
            print (f"Warning: Model {self .model_path2 } not found")
            self .model2 =None
        self .card_collection =self ._load_card_collection ()
        self .image_names =self ._load_image_names ()
        self .opponent_cards =['MysteryCard']*8
        self .temp_opponent_cards =['MysteryCard']*8
        self .continuous_classification_count =[0 ]*8
        self .required_continuous_classification_count =3
        self .opponent_hand =['MysteryCard']*8
        self .pending =[]
    def _load_card_collection (self ):
        card_collection ={}
        if os .path .exists (self .card_collection_path ):
            with open (self .card_collection_path ,'r')as f :
                for line in f :
                    if ':'in line :
                        key ,value =line .split (':',1 )
                        try :
                            card_collection [key .strip ()]=int (value .strip ().split ('/')[0 ])
                        except :
                            pass
        return card_collection
    def _load_image_names (self ):
        return []
    def preprocess_card_image (self ,img ,size =(32 ,32 )):
        img =cv2 .resize (img ,size )
        img =img .astype ("float")/255.0
        img =img_to_array (img )
        img =np .expand_dims (img ,axis =0 )
        return img
    def detect_card (self ,card_image ,slot_index ):
        if self .model1 is None :
            return None
        if self .opponent_cards [slot_index ]!="MysteryCard":
            return self .opponent_cards [slot_index ]
        img =self .preprocess_card_image (card_image )
        output =self .model1 .predict (img ,verbose =0 )[0 ]
        label =output .argmax ()
        if len (self .image_names )>label :
            predicted_card =self .image_names [label ]
        else :
            return None
        if predicted_card =="MysteryCard":
            return None
        if self .temp_opponent_cards [slot_index ]==predicted_card :
            if self .continuous_classification_count [slot_index ]==self .required_continuous_classification_count :
                self .opponent_cards [slot_index ]=predicted_card
                return predicted_card
            else :
                self .continuous_classification_count [slot_index ]+=1
        else :
            self .temp_opponent_cards [slot_index ]=predicted_card
            self .continuous_classification_count [slot_index ]=0
        return None
    def detect_card_placement (self ,card_image ,slot_index ):
        if self .model2 is None :
            return False
        img =self .preprocess_card_image (card_image ,size =(28 ,28 ))
        output =self .model2 .predict (img ,verbose =0 )[0 ]
        label =output .argmax ()
        if label ==1 or (label ==0 and output [label ]<0.80 ):
            return True
        return False
    def update_opponent_hand (self ,placed_card_index ):
        if placed_card_index in self .pending :
            self .pending .remove (placed_card_index )
            return
        if self .opponent_cards [placed_card_index ]!="MysteryCard":
            if self .opponent_cards [placed_card_index ]in self .opponent_hand [:4 ]:
                self .opponent_hand .remove (self .opponent_cards [placed_card_index ])
                self .opponent_hand .append (self .opponent_cards [placed_card_index ])
    def get_opponent_elixir (self ,current_elixir ,time_elapsed ,is_overtime =False ):
        if is_overtime :
            elixir_ratio =1 /0.9
        elif time_elapsed >120 :
            elixir_ratio =1 /1.4
        else :
            elixir_ratio =1 /2.8
        elixir =current_elixir +elixir_ratio *time_elapsed
        return min (elixir ,10.0 )
    def get_opponent_hand (self ):
        return self .opponent_hand [:4 ]
    def get_opponent_deck (self ):
        return self .opponent_cards .copy ()