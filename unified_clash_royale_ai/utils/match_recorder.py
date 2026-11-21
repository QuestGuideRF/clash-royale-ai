import os
import json
import cv2
import numpy as np
from datetime import datetime
class MatchRecorder :
    def __init__ (self ,save_dir ="recordings"):
        self .save_dir =save_dir
        self .is_recording =False
        self .current_match =None
        self .frames =[]
        self .actions =[]
        self .states =[]
        os .makedirs (save_dir ,exist_ok =True )
    def start_recording (self ,match_id =None ):
        if match_id is None :
            match_id =datetime .now ().strftime ('%Y%m%d_%H%M%S')
        self .current_match =match_id
        self .is_recording =True
        self .frames =[]
        self .actions =[]
        self .states =[]
        self .match_dir =os .path .join (self .save_dir ,match_id )
        os .makedirs (self .match_dir ,exist_ok =True )
        os .makedirs (os .path .join (self .match_dir ,'frames'),exist_ok =True )
        return match_id
    def record_frame (self ,frame ,timestamp ):
        if not self .is_recording :
            return
        self .frames .append ({
        'timestamp':timestamp ,
        'frame_id':len (self .frames )
        })
        frame_path =os .path .join (
        self .match_dir ,'frames',
        f"frame_{len (self .frames ):06d}.png"
        )
        cv2 .imwrite (frame_path ,frame )
    def record_action (self ,action ,game_state ,timestamp ):
        if not self .is_recording :
            return
        self .actions .append ({
        'timestamp':timestamp ,
        'action':action ,
        'frame_id':len (self .frames )-1
        })
        self .states .append ({
        'timestamp':timestamp ,
        'state':game_state ,
        'frame_id':len (self .frames )-1
        })
    def stop_recording (self ,result =None ):
        if not self .is_recording :
            return None
        self .is_recording =False
        metadata ={
        'match_id':self .current_match ,
        'total_frames':len (self .frames ),
        'total_actions':len (self .actions ),
        'result':result ,
        'recorded_at':datetime .now ().isoformat ()
        }
        with open (os .path .join (self .match_dir ,'metadata.json'),'w')as f :
            json .dump (metadata ,f ,indent =2 )
        with open (os .path .join (self .match_dir ,'actions.json'),'w')as f :
            json .dump (self .actions ,f ,indent =2 )
        with open (os .path .join (self .match_dir ,'states.json'),'w')as f :
            json .dump (self .states ,f ,indent =2 ,default =str )
        return self .match_dir
    def load_recording (self ,match_id ):
        match_dir =os .path .join (self .save_dir ,match_id )
        if not os .path .exists (match_dir ):
            return None
        with open (os .path .join (match_dir ,'metadata.json'),'r')as f :
            metadata =json .load (f )
        with open (os .path .join (match_dir ,'actions.json'),'r')as f :
            actions =json .load (f )
        with open (os .path .join (match_dir ,'states.json'),'r')as f :
            states =json .load (f )
        return {
        'metadata':metadata ,
        'actions':actions ,
        'states':states ,
        'frames_dir':os .path .join (match_dir ,'frames')
        }
    def list_recordings (self ):
        recordings =[]
        for item in os .listdir (self .save_dir ):
            item_path =os .path .join (self .save_dir ,item )
            if os .path .isdir (item_path ):
                metadata_path =os .path .join (item_path ,'metadata.json')
                if os .path .exists (metadata_path ):
                    with open (metadata_path ,'r')as f :
                        metadata =json .load (f )
                    recordings .append (metadata )
        return recordings