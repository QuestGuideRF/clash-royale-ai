import os
import json
from typing import Dict ,List ,Optional
class ProfileManager :
    PREDEFINED_PROFILES ={
    'fast':{
    'name':'Быстрый',
    'description':'Максимальная скорость, минимальная точность',
    'settings':{
    'screen_capture.target_fps':60 ,
    'recognition.confidence_threshold':0.5 ,
    'bot.mode':'fast',
    'bot.reaction_delay':0.05 ,
    'performance.parallel_processing':True ,
    'performance.num_workers':8
    }
    },
    'balanced':{
    'name':'Сбалансированный',
    'description':'Оптимальный баланс скорости и точности',
    'settings':{
    'screen_capture.target_fps':30 ,
    'recognition.confidence_threshold':0.7 ,
    'bot.mode':'balanced',
    'bot.reaction_delay':0.1 ,
    'performance.parallel_processing':True ,
    'performance.num_workers':4
    }
    },
    'accurate':{
    'name':'Точный',
    'description':'Максимальная точность, пониженная скорость',
    'settings':{
    'screen_capture.target_fps':15 ,
    'recognition.confidence_threshold':0.9 ,
    'bot.mode':'accurate',
    'bot.reaction_delay':0.2 ,
    'performance.parallel_processing':False ,
    'performance.num_workers':2
    }
    },
    'training':{
    'name':'Обучение',
    'description':'Для обучения моделей и сбора данных',
    'settings':{
    'screen_capture.target_fps':10 ,
    'recording.enabled':True ,
    'recording.save_frames':True ,
    'bot.auto_play':False ,
    'rl.enabled':True
    }
    },
    'low_end':{
    'name':'Слабый ПК',
    'description':'Для слабых компьютеров',
    'settings':{
    'screen_capture.target_fps':15 ,
    'screen_capture.method':'mss',
    'recognition.use_gpu':False ,
    'performance.cache_enabled':True ,
    'performance.num_workers':2
    }
    }
    }
    def __init__ (self ,profiles_dir ="config/profiles"):
        self .profiles_dir =profiles_dir
        os .makedirs (profiles_dir ,exist_ok =True )
        self .custom_profiles =self ._load_custom_profiles ()
        self .active_profile =None
    def _load_custom_profiles (self )->Dict :
        profiles ={}
        for filename in os .listdir (self .profiles_dir ):
            if filename .endswith ('.json'):
                profile_id =filename [:-5 ]
                path =os .path .join (self .profiles_dir ,filename )
                try :
                    with open (path ,'r',encoding ='utf-8')as f :
                        profiles [profile_id ]=json .load (f )
                except Exception as e :
                    print (f"Ошибка загрузки профиля {filename }: {e }")
        return profiles
    def get_all_profiles (self )->Dict :
        all_profiles =self .PREDEFINED_PROFILES .copy ()
        all_profiles .update (self .custom_profiles )
        return all_profiles
    def get_profile (self ,profile_id :str )->Optional [Dict ]:
        all_profiles =self .get_all_profiles ()
        return all_profiles .get (profile_id )
    def create_profile (self ,profile_id :str ,name :str ,
    description :str ,settings :Dict ):
        profile ={
        'name':name ,
        'description':description ,
        'settings':settings ,
        'custom':True
        }
        self .custom_profiles [profile_id ]=profile
        self ._save_profile (profile_id ,profile )
    def _save_profile (self ,profile_id :str ,profile :Dict ):
        path =os .path .join (self .profiles_dir ,f"{profile_id }.json")
        with open (path ,'w',encoding ='utf-8')as f :
            json .dump (profile ,f ,indent =2 ,ensure_ascii =False )
    def delete_profile (self ,profile_id :str )->bool :
        if profile_id in self .PREDEFINED_PROFILES :
            return False
        if profile_id in self .custom_profiles :
            del self .custom_profiles [profile_id ]
            path =os .path .join (self .profiles_dir ,f"{profile_id }.json")
            if os .path .exists (path ):
                os .remove (path )
            return True
        return False
    def apply_profile (self ,profile_id :str ,settings_manager )->bool :
        profile =self .get_profile (profile_id )
        if not profile :
            return False
        for path ,value in profile ['settings'].items ():
            settings_manager .set (path ,value )
        self .active_profile =profile_id
        return True
    def get_active_profile (self )->Optional [str ]:
        return self .active_profile
    def create_from_current (self ,settings_manager ,profile_id :str ,
    name :str ,description :str ):
        current =settings_manager .get_all ()
        flat_settings =self ._flatten_settings (current )
        self .create_profile (profile_id ,name ,description ,flat_settings )
    def _flatten_settings (self ,settings :Dict ,prefix :str ='')->Dict :
        flat ={}
        for key ,value in settings .items ():
            full_key =f"{prefix }.{key }"if prefix else key
            if isinstance (value ,dict ):
                flat .update (self ._flatten_settings (value ,full_key ))
            else :
                flat [full_key ]=value
        return flat
    def list_profiles (self )->List [Dict ]:
        profiles =[]
        for profile_id ,profile in self .get_all_profiles ().items ():
            profiles .append ({
            'id':profile_id ,
            'name':profile .get ('name',profile_id ),
            'description':profile .get ('description',''),
            'custom':profile .get ('custom',False ),
            'active':profile_id ==self .active_profile
            })
        return profiles