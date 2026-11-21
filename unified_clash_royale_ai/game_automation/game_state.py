import time
import cv2
import numpy as np
import os
import sys
try :
    import easyocr
except ImportError :
    easyocr =None
sys .path .insert (0 ,os .path .dirname (os .path .dirname (os .path .abspath (__file__ ))))
from unified_clash_royale_ai .config import (
ELIXIR_COOLDOWN_NORMAL ,ELIXIR_COOLDOWN_DOUBLE ,ELIXIR_COOLDOWN_OVERTIME ,
CARD_COSTS
)
class GameState :
    def __init__ (self ):
        self .elixir_blue =5
        self .elixir_red =5
        self .elixir_timer_blue =None
        self .elixir_timer_red =None
        self .elixir_cooldown =ELIXIR_COOLDOWN_NORMAL
        self .cards_in_hand ={0 :None ,1 :None ,2 :None ,3 :None }
        self .next_card =None
        self .towers_blue =3
        self .towers_red =3
        self .tower_hp_red ={0 :1512 ,1 :1512 ,2 :2568 }
        self .tower_hp_blue ={3 :2352 ,4 :2352 ,5 :3768 }
        self .position_towers_blue ={3 :(133 ,654 ),4 :(422 ,654 ),5 :(274 ,713 )}
        self .position_towers_red =[(133 ,242 ),(422 ,242 ),(274 ,161 )]
        self .chrono =180
        self .timer =None
        self .overtime =False
        self .blue_king_activated =False
        self .red_king_activated =False
        self .zone_placement_blue =[((77 ,480 ),(496 ,750 ))]
        self .reader =None
        if easyocr is not None :
            try :
                self .reader =easyocr .Reader (['en'])
            except Exception as e :
                print (f"Warning: Could not initialize OCR reader: {e }")
    def update_elixir (self ,screenshot ,is_blue =True ):
        empty_color =np .array ([123 ,54 ,5 ])
        color_tolerance =20
        x_coordinates =[183 ,222 ,261 ,300 ,339 ,378 ,417 ,456 ,495 ,534 ]
        y_base =993 if is_blue else 993
        def is_empty_square (px_color ):
            for i in range (3 ):
                if abs (px_color [i ]-empty_color [i ])>color_tolerance :
                    return False
            return True
        non_full_count =-1
        for x in x_coordinates :
            pass
        if is_blue :
            self .elixir_blue =non_full_count
            self .elixir_timer_blue =time .time ()
        else :
            self .elixir_red =non_full_count
            self .elixir_timer_red =time .time ()
    def update_timer (self ):
        if self .timer is None :
            self .timer =time .time ()
            return
        elapsed =time .time ()-self .timer
        if elapsed >=1 :
            self .chrono -=int (elapsed )
            self .timer =time .time ()-(elapsed %1 )
            if self .chrono <=60 :
                if self .overtime :
                    self .elixir_cooldown =ELIXIR_COOLDOWN_OVERTIME
                else :
                    self .elixir_cooldown =ELIXIR_COOLDOWN_DOUBLE
            elif self .chrono <=0 :
                if not self .overtime and self .towers_blue ==self .towers_red :
                    self .overtime =True
                    self .chrono =120
    def update_tower_hp (self ,tower_index ,hp ):
        if tower_index <3 :
            if self .tower_hp_red [tower_index ]and hp <self .tower_hp_red [tower_index ]:
                self .tower_hp_red [tower_index ]=hp
        else :
            if self .tower_hp_blue [tower_index ]and hp <self .tower_hp_blue [tower_index ]:
                self .tower_hp_blue [tower_index ]=hp
    def use_card (self ,card_slot_index ):
        card =self .cards_in_hand [card_slot_index ]
        if card and card in CARD_COSTS :
            cost =CARD_COSTS [card ]
            if self .elixir_blue >=cost :
                self .elixir_blue -=cost
                self .cards_in_hand [card_slot_index ]=None
                return True
        return False
    def get_state_dict (self ):
        return {
        'elixir_blue':self .elixir_blue ,
        'elixir_red':self .elixir_red ,
        'towers_blue':self .towers_blue ,
        'towers_red':self .towers_red ,
        'tower_hp_blue':self .tower_hp_blue .copy (),
        'tower_hp_red':self .tower_hp_red .copy (),
        'cards_in_hand':self .cards_in_hand .copy (),
        'chrono':self .chrono ,
        'overtime':self .overtime
        }