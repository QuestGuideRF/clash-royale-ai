import time
import hashlib
import pickle
import os
from collections import OrderedDict
from functools import wraps
import threading
class CacheManager :
    def __init__ (self ,max_size =1000 ,ttl =300 ,persist_path =None ):
        self .max_size =max_size
        self .ttl =ttl
        self .persist_path =persist_path
        self .cache =OrderedDict ()
        self .timestamps ={}
        self .hits =0
        self .misses =0
        self .lock =threading .Lock ()
        if persist_path and os .path .exists (persist_path ):
            self ._load_cache ()
    def _generate_key (self ,*args ,**kwargs ):
        key_data =pickle .dumps ((args ,sorted (kwargs .items ())))
        return hashlib .md5 (key_data ).hexdigest ()
    def get (self ,key ):
        with self .lock :
            if key not in self .cache :
                self .misses +=1
                return None
            if time .time ()-self .timestamps [key ]>self .ttl :
                del self .cache [key ]
                del self .timestamps [key ]
                self .misses +=1
                return None
            self .cache .move_to_end (key )
            self .hits +=1
            return self .cache [key ]
    def set (self ,key ,value ):
        with self .lock :
            if key in self .cache :
                del self .cache [key ]
            while len (self .cache )>=self .max_size :
                oldest_key =next (iter (self .cache ))
                del self .cache [oldest_key ]
                del self .timestamps [oldest_key ]
            self .cache [key ]=value
            self .timestamps [key ]=time .time ()
    def delete (self ,key ):
        with self .lock :
            if key in self .cache :
                del self .cache [key ]
                del self .timestamps [key ]
    def clear (self ):
        with self .lock :
            self .cache .clear ()
            self .timestamps .clear ()
    def cached (self ,ttl =None ):
        def decorator (func ):
            @wraps (func )
            def wrapper (*args ,**kwargs ):
                key =f"{func .__name__ }:{self ._generate_key (*args ,**kwargs )}"
                result =self .get (key )
                if result is not None :
                    return result
                result =func (*args ,**kwargs )
                old_ttl =self .ttl
                if ttl is not None :
                    self .ttl =ttl
                self .set (key ,result )
                self .ttl =old_ttl
                return result
            return wrapper
        return decorator
    def get_stats (self ):
        total =self .hits +self .misses
        hit_rate =self .hits /total if total >0 else 0
        return {
        'size':len (self .cache ),
        'max_size':self .max_size ,
        'hits':self .hits ,
        'misses':self .misses ,
        'hit_rate':hit_rate ,
        'ttl':self .ttl
        }
    def _save_cache (self ):
        if not self .persist_path :
            return
        with self .lock :
            data ={
            'cache':dict (self .cache ),
            'timestamps':dict (self .timestamps )
            }
            with open (self .persist_path ,'wb')as f :
                pickle .dump (data ,f )
    def _load_cache (self ):
        try :
            with open (self .persist_path ,'rb')as f :
                data =pickle .load (f )
            self .cache =OrderedDict (data ['cache'])
            self .timestamps =data ['timestamps']
            current_time =time .time ()
            expired =[
            k for k ,t in self .timestamps .items ()
            if current_time -t >self .ttl
            ]
            for k in expired :
                del self .cache [k ]
                del self .timestamps [k ]
        except Exception as e :
            print (f"Ошибка загрузки кэша: {e }")
    def cleanup_expired (self ):
        with self .lock :
            current_time =time .time ()
            expired =[
            k for k ,t in self .timestamps .items ()
            if current_time -t >self .ttl
            ]
            for k in expired :
                del self .cache [k ]
                del self .timestamps [k ]
            return len (expired )
class ImageCache (CacheManager ):
    def __init__ (self ,max_size =100 ,ttl =60 ):
        super ().__init__ (max_size =max_size ,ttl =ttl )
    def cache_frame (self ,frame_id ,frame_data ):
        self .set (f"frame_{frame_id }",frame_data )
    def get_frame (self ,frame_id ):
        return self .get (f"frame_{frame_id }")
    def cache_detection (self ,frame_id ,detection_type ,result ):
        key =f"detection_{frame_id }_{detection_type }"
        self .set (key ,result )
    def get_detection (self ,frame_id ,detection_type ):
        key =f"detection_{frame_id }_{detection_type }"
        return self .get (key )
class ModelPredictionCache (CacheManager ):
    def __init__ (self ,max_size =500 ,ttl =10 ):
        super ().__init__ (max_size =max_size ,ttl =ttl )
    def _hash_image (self ,image ):
        return hashlib .md5 (image .tobytes ()).hexdigest ()[:16 ]
    def cache_prediction (self ,model_name ,image ,prediction ):
        image_hash =self ._hash_image (image )
        key =f"{model_name }_{image_hash }"
        self .set (key ,prediction )
    def get_prediction (self ,model_name ,image ):
        image_hash =self ._hash_image (image )
        key =f"{model_name }_{image_hash }"
        return self .get (key )