import os
import json
import hashlib
import shutil
from datetime import datetime
from urllib .request import urlretrieve
from urllib .error import URLError
import threading
class ModelManager :
    MODEL_URLS ={
    'card_detector':'https://example.com/models/card_detector_v1.h5',
    'yolo_troops':'https://example.com/models/yolo_troops_v1.pt',
    'vae':'https://example.com/models/vae_v1.h5',
    'dqn':'https://example.com/models/dqn_v1.h5',
    }
    def __init__ (self ,models_dir ="models",cache_dir =".model_cache"):
        self .models_dir =models_dir
        self .cache_dir =cache_dir
        self .versions_file =os .path .join (models_dir ,'versions.json')
        os .makedirs (models_dir ,exist_ok =True )
        os .makedirs (cache_dir ,exist_ok =True )
        self .versions =self ._load_versions ()
    def _load_versions (self ):
        if os .path .exists (self .versions_file ):
            with open (self .versions_file ,'r')as f :
                return json .load (f )
        return {}
    def _save_versions (self ):
        with open (self .versions_file ,'w')as f :
            json .dump (self .versions ,f ,indent =2 )
    def _calculate_checksum (self ,file_path ):
        hash_md5 =hashlib .md5 ()
        with open (file_path ,'rb')as f :
            for chunk in iter (lambda :f .read (4096 ),b''):
                hash_md5 .update (chunk )
        return hash_md5 .hexdigest ()
    def register_model (self ,model_name ,model_path ,version =None ,metadata =None ):
        if not os .path .exists (model_path ):
            raise FileNotFoundError (f"Модель не найдена: {model_path }")
        if version is None :
            version =datetime .now ().strftime ("%Y%m%d_%H%M%S")
        checksum =self ._calculate_checksum (model_path )
        model_dir =os .path .join (self .models_dir ,model_name )
        os .makedirs (model_dir ,exist_ok =True )
        ext =os .path .splitext (model_path )[1 ]
        versioned_path =os .path .join (model_dir ,f"{model_name }_v{version }{ext }")
        shutil .copy2 (model_path ,versioned_path )
        if model_name not in self .versions :
            self .versions [model_name ]={'versions':[]}
        version_info ={
        'version':version ,
        'path':versioned_path ,
        'checksum':checksum ,
        'created_at':datetime .now ().isoformat (),
        'metadata':metadata or {}
        }
        self .versions [model_name ]['versions'].append (version_info )
        self .versions [model_name ]['latest']=version
        self ._save_versions ()
        return version_info
    def get_model_path (self ,model_name ,version ='latest'):
        if model_name not in self .versions :
            return None
        if version =='latest':
            version =self .versions [model_name ].get ('latest')
        for v in self .versions [model_name ]['versions']:
            if v ['version']==version :
                return v ['path']
        return None
    def download_model (self ,model_name ,url =None ,force =False ):
        if url is None :
            url =self .MODEL_URLS .get (model_name )
        if url is None :
            raise ValueError (f"URL не найден для модели: {model_name }")
        cache_path =os .path .join (self .cache_dir ,f"{model_name }_cached")
        if os .path .exists (cache_path )and not force :
            print (f"Модель {model_name } найдена в кэше")
            return cache_path
        print (f"Загрузка модели {model_name } из {url }...")
        try :
            def progress_hook (count ,block_size ,total_size ):
                percent =int (count *block_size *100 /total_size )
                print (f"\rПрогресс: {percent }%",end ='',flush =True )
            urlretrieve (url ,cache_path ,reporthook =progress_hook )
            print ("\nЗагрузка завершена!")
            self .register_model (model_name ,cache_path ,metadata ={'source':url })
            return cache_path
        except URLError as e :
            print (f"Ошибка загрузки: {e }")
            return None
    def auto_load_models (self ,required_models =None ):
        if required_models is None :
            required_models =['card_detector','yolo_troops']
        loaded ={}
        for model_name in required_models :
            model_path =self .get_model_path (model_name )
            if model_path and os .path .exists (model_path ):
                print (f"✓ Модель {model_name } найдена локально")
                loaded [model_name ]=model_path
            else :
                print (f"⬇ Загрузка модели {model_name }...")
                path =self .download_model (model_name )
                if path :
                    loaded [model_name ]=path
                else :
                    print (f"✗ Не удалось загрузить {model_name }")
        return loaded
    def list_versions (self ,model_name ):
        if model_name not in self .versions :
            return []
        return self .versions [model_name ]['versions']
    def delete_version (self ,model_name ,version ):
        if model_name not in self .versions :
            return False
        for i ,v in enumerate (self .versions [model_name ]['versions']):
            if v ['version']==version :
                if os .path .exists (v ['path']):
                    os .remove (v ['path'])
                del self .versions [model_name ]['versions'][i ]
                if self .versions [model_name ]['latest']==version :
                    if self .versions [model_name ]['versions']:
                        self .versions [model_name ]['latest']=self .versions [model_name ]['versions'][-1 ]['version']
                    else :
                        del self .versions [model_name ]
                self ._save_versions ()
                return True
        return False
    def cleanup_old_versions (self ,model_name ,keep_count =3 ):
        if model_name not in self .versions :
            return
        versions =self .versions [model_name ]['versions']
        if len (versions )<=keep_count :
            return
        to_delete =versions [:-keep_count ]
        for v in to_delete :
            self .delete_version (model_name ,v ['version'])