import time
import statistics
import numpy as np
import gc
class Benchmarker :
    def __init__ (self ):
        self .results ={}
    def benchmark (self ,func ,*args ,iterations =100 ,warmup =10 ,**kwargs ):
        for _ in range (warmup ):
            func (*args ,**kwargs )
        gc .collect ()
        times =[]
        for _ in range (iterations ):
            start =time .perf_counter ()
            func (*args ,**kwargs )
            elapsed =time .perf_counter ()-start
            times .append (elapsed )
        result ={
        'name':func .__name__ if hasattr (func ,'__name__')else str (func ),
        'iterations':iterations ,
        'total_time':sum (times ),
        'mean':statistics .mean (times ),
        'median':statistics .median (times ),
        'std':statistics .stdev (times )if len (times )>1 else 0 ,
        'min':min (times ),
        'max':max (times ),
        'fps':1 /statistics .mean (times )if statistics .mean (times )>0 else 0
        }
        self .results [result ['name']]=result
        return result
    def benchmark_screen_capture (self ,iterations =100 ):
        from ..performance .screen_optimizer import ScreenOptimizer
        results ={}
        for method in ['mss','dxcam']:
            try :
                optimizer =ScreenOptimizer (method =method )
                for _ in range (10 ):
                    optimizer .capture ()
                times =[]
                for _ in range (iterations ):
                    start =time .perf_counter ()
                    optimizer .capture ()
                    times .append (time .perf_counter ()-start )
                results [method ]={
                'mean_ms':statistics .mean (times )*1000 ,
                'fps':1 /statistics .mean (times ),
                'min_ms':min (times )*1000 ,
                'max_ms':max (times )*1000
                }
                optimizer .cleanup ()
            except Exception as e :
                results [method ]={'error':str (e )}
        return results
    def benchmark_image_processing (self ,iterations =100 ):
        import cv2
        test_image =np .random .randint (0 ,255 ,(1024 ,600 ,3 ),dtype =np .uint8 )
        operations ={
        'resize_480':lambda img :cv2 .resize (img ,(480 ,640 )),
        'resize_240':lambda img :cv2 .resize (img ,(240 ,320 )),
        'grayscale':lambda img :cv2 .cvtColor (img ,cv2 .COLOR_BGR2GRAY ),
        'blur':lambda img :cv2 .GaussianBlur (img ,(5 ,5 ),0 ),
        'canny':lambda img :cv2 .Canny (cv2 .cvtColor (img ,cv2 .COLOR_BGR2GRAY ),50 ,150 ),
        'threshold':lambda img :cv2 .threshold (
        cv2 .cvtColor (img ,cv2 .COLOR_BGR2GRAY ),127 ,255 ,cv2 .THRESH_BINARY
        )[1 ]
        }
        results ={}
        for name ,op in operations .items ():
            times =[]
            for _ in range (iterations ):
                start =time .perf_counter ()
                op (test_image )
                times .append (time .perf_counter ()-start )
            results [name ]={
            'mean_ms':statistics .mean (times )*1000 ,
            'fps':1 /statistics .mean (times )
            }
        return results
    def benchmark_cache (self ,iterations =10000 ):
        from ..performance .cache_manager import CacheManager
        cache =CacheManager (max_size =1000 )
        for i in range (1000 ):
            cache .set (f'key_{i }',f'value_{i }')
        read_times =[]
        for _ in range (iterations ):
            key =f'key_{np .random .randint (0 ,1000 )}'
            start =time .perf_counter ()
            cache .get (key )
            read_times .append (time .perf_counter ()-start )
        write_times =[]
        for i in range (iterations ):
            start =time .perf_counter ()
            cache .set (f'new_key_{i }',f'new_value_{i }')
            write_times .append (time .perf_counter ()-start )
        return {
        'read':{
        'mean_us':statistics .mean (read_times )*1_000_000 ,
        'ops_per_sec':1 /statistics .mean (read_times )
        },
        'write':{
        'mean_us':statistics .mean (write_times )*1_000_000 ,
        'ops_per_sec':1 /statistics .mean (write_times )
        }
        }
    def benchmark_neural_network (self ,model_path =None ,iterations =100 ):
        results ={}
        batch_sizes =[1 ,8 ,16 ,32 ]
        input_shape =(32 ,32 ,3 )
        try :
            import tensorflow as tf
            if model_path is None :
                model =tf .keras .Sequential ([
                tf .keras .layers .Conv2D (32 ,3 ,activation ='relu',input_shape =input_shape ),
                tf .keras .layers .MaxPooling2D (),
                tf .keras .layers .Flatten (),
                tf .keras .layers .Dense (10 ,activation ='softmax')
                ])
            else :
                model =tf .keras .models .load_model (model_path )
            for batch_size in batch_sizes :
                test_input =np .random .random ((batch_size ,)+input_shape ).astype (np .float32 )
                for _ in range (10 ):
                    model .predict (test_input ,verbose =0 )
                times =[]
                for _ in range (iterations ):
                    start =time .perf_counter ()
                    model .predict (test_input ,verbose =0 )
                    times .append (time .perf_counter ()-start )
                results [f'batch_{batch_size }']={
                'mean_ms':statistics .mean (times )*1000 ,
                'fps':batch_size /statistics .mean (times )
                }
        except ImportError :
            results ['error']='TensorFlow не установлен'
        return results
    def run_full_benchmark (self ):
        print ("="*60 )
        print ("ПОЛНЫЙ БЕНЧМАРК ПРОИЗВОДИТЕЛЬНОСТИ")
        print ("="*60 )
        results ={}
        print ("\n📷 Обработка изображений...")
        results ['image_processing']=self .benchmark_image_processing ()
        print ("💾 Кэш...")
        results ['cache']=self .benchmark_cache ()
        print ("🧠 Нейронная сеть...")
        results ['neural_network']=self .benchmark_neural_network ()
        print ("\n"+"="*60 )
        print ("РЕЗУЛЬТАТЫ")
        print ("="*60 )
        for category ,cat_results in results .items ():
            print (f"\n{category .upper ()}:")
            if 'error'in cat_results :
                print (f"  Ошибка: {cat_results ['error']}")
            else :
                for key ,value in cat_results .items ():
                    if isinstance (value ,dict ):
                        print (f"  {key }:")
                        for k ,v in value .items ():
                            print (f"    {k }: {v :.2f}")
                    else :
                        print (f"  {key }: {value }")
        return results
    def generate_report (self ):
        report =[]
        report .append ("="*60 )
        report .append ("СРАВНИТЕЛЬНЫЙ ОТЧЕТ")
        report .append ("="*60 )
        for name ,result in self .results .items ():
            report .append (f"\n{name }:")
            report .append (f"  Iterations: {result ['iterations']}")
            report .append (f"  Mean: {result ['mean']*1000 :.3f}ms")
            report .append (f"  Median: {result ['median']*1000 :.3f}ms")
            report .append (f"  Std: {result ['std']*1000 :.3f}ms")
            report .append (f"  Min: {result ['min']*1000 :.3f}ms")
            report .append (f"  Max: {result ['max']*1000 :.3f}ms")
            report .append (f"  FPS: {result ['fps']:.1f}")
        return "\n".join (report )