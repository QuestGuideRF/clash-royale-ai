import os
import json
from datetime import datetime
import numpy as np
class ReplayParser :
    def __init__ (self ,recordings_dir ="recordings"):
        self .recordings_dir =recordings_dir
    def load_replay (self ,match_id ):
        match_dir =os .path .join (self .recordings_dir ,match_id )
        if not os .path .exists (match_dir ):
            raise FileNotFoundError (f"Реплей не найден: {match_id }")
        replay ={
        'match_id':match_id ,
        'metadata':None ,
        'actions':[],
        'states':[],
        'frames_dir':os .path .join (match_dir ,'frames')
        }
        metadata_path =os .path .join (match_dir ,'metadata.json')
        if os .path .exists (metadata_path ):
            with open (metadata_path ,'r')as f :
                replay ['metadata']=json .load (f )
        actions_path =os .path .join (match_dir ,'actions.json')
        if os .path .exists (actions_path ):
            with open (actions_path ,'r')as f :
                replay ['actions']=json .load (f )
        states_path =os .path .join (match_dir ,'states.json')
        if os .path .exists (states_path ):
            with open (states_path ,'r')as f :
                replay ['states']=json .load (f )
        return Replay (replay )
    def list_replays (self ,limit =None ,filter_result =None ):
        replays =[]
        if not os .path .exists (self .recordings_dir ):
            return replays
        for item in os .listdir (self .recordings_dir ):
            item_path =os .path .join (self .recordings_dir ,item )
            if os .path .isdir (item_path ):
                metadata_path =os .path .join (item_path ,'metadata.json')
                if os .path .exists (metadata_path ):
                    with open (metadata_path ,'r')as f :
                        metadata =json .load (f )
                    if filter_result and metadata .get ('result')!=filter_result :
                        continue
                    replays .append ({
                    'match_id':item ,
                    'metadata':metadata
                    })
        replays .sort (key =lambda x :x ['metadata'].get ('recorded_at',''),reverse =True )
        if limit :
            replays =replays [:limit ]
        return replays
    def parse_actions (self ,replay ):
        parsed_actions =[]
        for action in replay .actions :
            parsed ={
            'timestamp':action .get ('timestamp'),
            'frame_id':action .get ('frame_id'),
            'action_type':'card_play'if action .get ('action')else 'none',
            'details':action .get ('action',{})
            }
            parsed_actions .append (parsed )
        return parsed_actions
    def get_timeline (self ,replay ):
        timeline =[]
        for state in replay .states :
            event ={
            'timestamp':state .get ('timestamp'),
            'frame_id':state .get ('frame_id'),
            'game_state':state .get ('state',{})
            }
            timeline .append (event )
        return timeline
class Replay :
    def __init__ (self ,data ):
        self .match_id =data .get ('match_id')
        self .metadata =data .get ('metadata',{})
        self .actions =data .get ('actions',[])
        self .states =data .get ('states',[])
        self .frames_dir =data .get ('frames_dir')
    @property
    def duration (self ):
        if not self .states :
            return 0
        first =self .states [0 ].get ('timestamp',0 )
        last =self .states [-1 ].get ('timestamp',0 )
        return last -first
    @property
    def result (self ):
        return self .metadata .get ('result')
    @property
    def total_actions (self ):
        return len (self .actions )
    @property
    def total_frames (self ):
        return self .metadata .get ('total_frames',0 )
    def get_frame_path (self ,frame_id ):
        return os .path .join (self .frames_dir ,f'frame_{frame_id :06d}.png')
    def get_action_at_frame (self ,frame_id ):
        for action in self .actions :
            if action .get ('frame_id')==frame_id :
                return action
        return None
    def get_state_at_frame (self ,frame_id ):
        for state in self .states :
            if state .get ('frame_id')==frame_id :
                return state
        return None