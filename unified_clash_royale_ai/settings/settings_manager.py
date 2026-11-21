import os
import json
from typing import Any ,Dict ,Optional
class SettingsManager :
    DEFAULT_SETTINGS ={
    'general':{
    'language':'ru',
    'theme':'dark',
    'log_level':'INFO',
    'auto_start':False ,
    'minimize_to_tray':True
    },
    'screen_capture':{
    'method':'auto',
    'target_fps':30 ,
    'window_title':'BlueStacks',
    'region':None
    },
    'recognition':{
    'card_model':'default',
    'troop_model':'yolov8n',
    'confidence_threshold':0.7 ,
    'use_gpu':True
    },
    'bot':{
    'mode':'balanced',
    'auto_play':False ,
    'reaction_delay':0.1 ,
    'random_delay':0.05
    },
    'rl':{
    'enabled':False ,
    'learning_rate':0.001 ,
    'epsilon':0.1 ,
    'model_path':None
    },
    'recording':{
    'enabled':True ,
    'save_frames':True ,
    'save_actions':True ,
    'directory':'recordings'
    },
    'performance':{
    'cache_enabled':True ,
    'cache_size':1000 ,
    'parallel_processing':True ,
    'num_workers':4
    },
    'hotkeys':{
    'start_stop':'F5',
    'pause':'F6',
    'screenshot':'F7',
    'settings':'F8'
    }
    }
    def __init__ (self ,config_path ="config/settings.json"):
        self .config_path =config_path
        self .settings =self ._load_settings ()
        self ._callbacks ={}
    def _load_settings (self )->Dict :
        if os .path .exists (self .config_path ):
            try :
                with open (self .config_path ,'r',encoding ='utf-8')as f :
                    loaded =json .load (f )
                    return self ._merge_settings (self .DEFAULT_SETTINGS .copy (),loaded )
            except Exception as e :
                print (f"Ошибка загрузки настроек: {e }")
        return self .DEFAULT_SETTINGS .copy ()
    def _merge_settings (self ,base :Dict ,override :Dict )->Dict :
        result =base .copy ()
        for key ,value in override .items ():
            if key in result and isinstance (result [key ],dict )and isinstance (value ,dict ):
                result [key ]=self ._merge_settings (result [key ],value )
            else :
                result [key ]=value
        return result
    def save (self ):
        os .makedirs (os .path .dirname (self .config_path )or '.',exist_ok =True )
        with open (self .config_path ,'w',encoding ='utf-8')as f :
            json .dump (self .settings ,f ,indent =2 ,ensure_ascii =False )
    def get (self ,path :str ,default :Any =None )->Any :
        keys =path .split ('.')
        value =self .settings
        for key in keys :
            if isinstance (value ,dict )and key in value :
                value =value [key ]
            else :
                return default
        return value
    def set (self ,path :str ,value :Any ):
        keys =path .split ('.')
        current =self .settings
        for key in keys [:-1 ]:
            if key not in current :
                current [key ]={}
            current =current [key ]
        old_value =current .get (keys [-1 ])
        current [keys [-1 ]]=value
        if path in self ._callbacks and old_value !=value :
            for callback in self ._callbacks [path ]:
                callback (value ,old_value )
        self .save ()
    def on_change (self ,path :str ,callback ):
        if path not in self ._callbacks :
            self ._callbacks [path ]=[]
        self ._callbacks [path ].append (callback )
    def reset (self ,section :str =None ):
        if section :
            if section in self .DEFAULT_SETTINGS :
                self .settings [section ]=self .DEFAULT_SETTINGS [section ].copy ()
        else :
            self .settings =self .DEFAULT_SETTINGS .copy ()
        self .save ()
    def export_settings (self ,path :str ):
        with open (path ,'w',encoding ='utf-8')as f :
            json .dump (self .settings ,f ,indent =2 ,ensure_ascii =False )
    def import_settings (self ,path :str ):
        with open (path ,'r',encoding ='utf-8')as f :
            imported =json .load (f )
            self .settings =self ._merge_settings (self .DEFAULT_SETTINGS .copy (),imported )
            self .save ()
    def get_all (self )->Dict :
        return self .settings .copy ()
_settings_instance =None
def get_settings ()->SettingsManager :
    global _settings_instance
    if _settings_instance is None :
        _settings_instance =SettingsManager ()
    return _settings_instance