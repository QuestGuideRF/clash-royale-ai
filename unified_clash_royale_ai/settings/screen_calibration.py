import json
import os
try :
    import cv2
    import numpy as np
    HAS_CV2 =True
except ImportError :
    HAS_CV2 =False
class ScreenCalibrator :
    REFERENCE_WIDTH =480
    REFERENCE_HEIGHT =854
    REFERENCE_COORDS ={
    'card_slots':[
    (125 ,848 ,221 ,971 ),
    (229 ,848 ,325 ,971 ),
    (333 ,848 ,429 ,971 ),
    (437 ,848 ,533 ,971 ),
    ],
    'elixir_bar':(96 ,987 ,450 ,1000 ),
    'timer':(200 ,15 ,280 ,45 ),
    'tower_hp_ally_left':(60 ,600 ,140 ,620 ),
    'tower_hp_ally_right':(340 ,600 ,420 ,620 ),
    'tower_hp_ally_king':(200 ,700 ,280 ,720 ),
    'tower_hp_enemy_left':(60 ,150 ,140 ,170 ),
    'tower_hp_enemy_right':(340 ,150 ,420 ,170 ),
    'tower_hp_enemy_king':(200 ,80 ,280 ,100 ),
    'battlefield':(0 ,100 ,480 ,750 ),
    'next_card':(30 ,848 ,90 ,920 )
    }
    def __init__ (self ,calibration_file ="config/calibration.json"):
        self .calibration_file =calibration_file
        self .calibration =self ._load_calibration ()
    def _load_calibration (self ):
        if os .path .exists (self .calibration_file ):
            with open (self .calibration_file ,'r')as f :
                return json .load (f )
        return {
        'screen_width':self .REFERENCE_WIDTH ,
        'screen_height':self .REFERENCE_HEIGHT ,
        'offset_x':0 ,
        'offset_y':0 ,
        'scale_x':1.0 ,
        'scale_y':1.0 ,
        'coords':self .REFERENCE_COORDS .copy ()
        }
    def save_calibration (self ):
        os .makedirs (os .path .dirname (self .calibration_file )or '.',exist_ok =True )
        with open (self .calibration_file ,'w')as f :
            json .dump (self .calibration ,f ,indent =2 )
    def auto_detect (self ,screenshot ):
        if not HAS_CV2 :
            return False
        height ,width =screenshot .shape [:2 ]
        self .calibration ['screen_width']=width
        self .calibration ['screen_height']=height
        self .calibration ['scale_x']=width /self .REFERENCE_WIDTH
        self .calibration ['scale_y']=height /self .REFERENCE_HEIGHT
        self ._recalculate_coords ()
        self .save_calibration ()
        return True
    def _recalculate_coords (self ):
        scale_x =self .calibration ['scale_x']
        scale_y =self .calibration ['scale_y']
        offset_x =self .calibration ['offset_x']
        offset_y =self .calibration ['offset_y']
        new_coords ={}
        for key ,value in self .REFERENCE_COORDS .items ():
            if isinstance (value ,list ):
                new_coords [key ]=[
                self ._scale_rect (rect ,scale_x ,scale_y ,offset_x ,offset_y )
                for rect in value
                ]
            else :
                new_coords [key ]=self ._scale_rect (
                value ,scale_x ,scale_y ,offset_x ,offset_y
                )
        self .calibration ['coords']=new_coords
    def _scale_rect (self ,rect ,scale_x ,scale_y ,offset_x ,offset_y ):
        x1 ,y1 ,x2 ,y2 =rect
        return (
        int (x1 *scale_x +offset_x ),
        int (y1 *scale_y +offset_y ),
        int (x2 *scale_x +offset_x ),
        int (y2 *scale_y +offset_y )
        )
    def set_offset (self ,x ,y ):
        self .calibration ['offset_x']=x
        self .calibration ['offset_y']=y
        self ._recalculate_coords ()
        self .save_calibration ()
    def get_coords (self ,element ):
        return self .calibration ['coords'].get (element )
    def get_card_position (self ,slot_index ):
        card_slots =self .get_coords ('card_slots')
        if card_slots and 0 <=slot_index <len (card_slots ):
            x1 ,y1 ,x2 ,y2 =card_slots [slot_index ]
            return ((x1 +x2 )//2 ,(y1 +y2 )//2 )
        return None
    def get_battlefield_position (self ,normalized_x ,normalized_y ):
        battlefield =self .get_coords ('battlefield')
        if battlefield :
            x1 ,y1 ,x2 ,y2 =battlefield
            x =int (x1 +(x2 -x1 )*normalized_x )
            y =int (y1 +(y2 -y1 )*normalized_y )
            return (x ,y )
        return None
    def manual_calibration (self ,points ):
        if 'top_left'in points and 'bottom_right'in points :
            tl =points ['top_left']
            br =points ['bottom_right']
            actual_width =br [0 ]-tl [0 ]
            actual_height =br [1 ]-tl [1 ]
            self .calibration ['offset_x']=tl [0 ]
            self .calibration ['offset_y']=tl [1 ]
            self .calibration ['screen_width']=actual_width
            self .calibration ['screen_height']=actual_height
            self .calibration ['scale_x']=actual_width /self .REFERENCE_WIDTH
            self .calibration ['scale_y']=actual_height /self .REFERENCE_HEIGHT
            self ._recalculate_coords ()
            self .save_calibration ()
    def test_calibration (self ,screenshot ):
        if not HAS_CV2 :
            return screenshot
        result =screenshot .copy ()
        for key ,value in self .calibration ['coords'].items ():
            if isinstance (value ,list ):
                for i ,rect in enumerate (value ):
                    x1 ,y1 ,x2 ,y2 =rect
                    cv2 .rectangle (result ,(x1 ,y1 ),(x2 ,y2 ),(0 ,255 ,0 ),2 )
                    cv2 .putText (result ,f"{key }_{i }",(x1 ,y1 -5 ),
                    cv2 .FONT_HERSHEY_SIMPLEX ,0.4 ,(0 ,255 ,0 ),1 )
            else :
                x1 ,y1 ,x2 ,y2 =value
                cv2 .rectangle (result ,(x1 ,y1 ),(x2 ,y2 ),(255 ,0 ,0 ),2 )
                cv2 .putText (result ,key ,(x1 ,y1 -5 ),
                cv2 .FONT_HERSHEY_SIMPLEX ,0.4 ,(255 ,0 ,0 ),1 )
        return result
    def get_calibration_status (self ):
        return {
        'screen_size':(
        self .calibration ['screen_width'],
        self .calibration ['screen_height']
        ),
        'scale':(
        self .calibration ['scale_x'],
        self .calibration ['scale_y']
        ),
        'offset':(
        self .calibration ['offset_x'],
        self .calibration ['offset_y']
        ),
        'elements_count':len (self .calibration ['coords'])
        }