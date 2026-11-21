import os
import numpy as np
try :
    import tensorflow as tf
    HAS_TF =True
except ImportError :
    HAS_TF =False
try :
    import onnx
    import onnxruntime as ort
    HAS_ONNX =True
except ImportError :
    HAS_ONNX =False
try :
    import tensorrt as trt
    HAS_TENSORRT =True
except ImportError :
    HAS_TENSORRT =False
class NeuralOptimizer :
    def __init__ (self ,models_dir ="models/optimized"):
        self .models_dir =models_dir
        os .makedirs (models_dir ,exist_ok =True )
        self .available_backends ={
        'tensorflow':HAS_TF ,
        'onnx':HAS_ONNX ,
        'tensorrt':HAS_TENSORRT
        }
    def convert_to_onnx (self ,model ,output_name ,input_shape =None ):
        if not HAS_TF or not HAS_ONNX :
            raise ImportError ("Требуется tensorflow и onnx")
        output_path =os .path .join (self .models_dir ,f"{output_name }.onnx")
        try :
            import tf2onnx
            spec =(tf .TensorSpec (input_shape ,tf .float32 ,name ="input"),)
            model_proto ,_ =tf2onnx .convert .from_keras (
            model ,
            input_signature =spec ,
            output_path =output_path
            )
            return output_path
        except ImportError :
            saved_model_path =os .path .join (self .models_dir ,"temp_saved_model")
            model .save (saved_model_path )
            import subprocess
            subprocess .run ([
            "python","-m","tf2onnx.convert",
            "--saved-model",saved_model_path ,
            "--output",output_path
            ])
            return output_path
    def optimize_onnx (self ,onnx_path ,output_path =None ):
        if not HAS_ONNX :
            raise ImportError ("Требуется onnx")
        import onnxoptimizer
        model =onnx .load (onnx_path )
        passes =[
        'eliminate_identity',
        'eliminate_nop_dropout',
        'eliminate_nop_transpose',
        'eliminate_deadend',
        'fuse_consecutive_squeezes',
        'fuse_consecutive_transposes',
        'fuse_add_bias_into_conv',
        'fuse_transpose_into_gemm'
        ]
        optimized =onnxoptimizer .optimize (model ,passes )
        if output_path is None :
            output_path =onnx_path .replace ('.onnx','_optimized.onnx')
        onnx .save (optimized ,output_path )
        return output_path
    def convert_to_tensorrt (self ,onnx_path ,output_path =None ,fp16 =True ):
        if not HAS_TENSORRT :
            raise ImportError ("Требуется tensorrt")
        TRT_LOGGER =trt .Logger (trt .Logger .WARNING )
        with trt .Builder (TRT_LOGGER )as builder :
            network_flags =1 <<int (trt .NetworkDefinitionCreationFlag .EXPLICIT_BATCH )
            with builder .create_network (network_flags )as network :
                with trt .OnnxParser (network ,TRT_LOGGER )as parser :
                    with open (onnx_path ,'rb')as f :
                        if not parser .parse (f .read ()):
                            for error in range (parser .num_errors ):
                                print (parser .get_error (error ))
                            return None
                    config =builder .create_builder_config ()
                    config .max_workspace_size =1 <<30
                    if fp16 and builder .platform_has_fast_fp16 :
                        config .set_flag (trt .BuilderFlag .FP16 )
                    engine =builder .build_engine (network ,config )
                    if output_path is None :
                        output_path =onnx_path .replace ('.onnx','.trt')
                    with open (output_path ,'wb')as f :
                        f .write (engine .serialize ())
                    return output_path
    def create_onnx_session (self ,onnx_path ,use_gpu =True ):
        if not HAS_ONNX :
            raise ImportError ("Требуется onnxruntime")
        providers =['CUDAExecutionProvider','CPUExecutionProvider']if use_gpu else ['CPUExecutionProvider']
        session_options =ort .SessionOptions ()
        session_options .graph_optimization_level =ort .GraphOptimizationLevel .ORT_ENABLE_ALL
        session_options .intra_op_num_threads =4
        session =ort .InferenceSession (
        onnx_path ,
        sess_options =session_options ,
        providers =providers
        )
        return session
    def quantize_model (self ,model ,method ='dynamic'):
        if not HAS_TF :
            raise ImportError ("Требуется tensorflow")
        if method =='dynamic':
            converter =tf .lite .TFLiteConverter .from_keras_model (model )
            converter .optimizations =[tf .lite .Optimize .DEFAULT ]
            quantized =converter .convert ()
        elif method =='static':
            converter =tf .lite .TFLiteConverter .from_keras_model (model )
            converter .optimizations =[tf .lite .Optimize .DEFAULT ]
            converter .representative_dataset =self ._get_representative_dataset
            converter .target_spec .supported_ops =[tf .lite .OpsSet .TFLITE_BUILTINS_INT8 ]
            converter .inference_input_type =tf .int8
            converter .inference_output_type =tf .int8
            quantized =converter .convert ()
        else :
            raise ValueError (f"Неизвестный метод: {method }")
        return quantized
    def _get_representative_dataset (self ):
        for _ in range (100 ):
            yield [np .random .random ((1 ,32 ,32 ,3 )).astype (np .float32 )]
    def benchmark_model (self ,model_path ,input_shape ,iterations =100 ):
        import time
        ext =os .path .splitext (model_path )[1 ]
        if ext =='.onnx':
            session =self .create_onnx_session (model_path )
            input_name =session .get_inputs ()[0 ].name
            dummy_input =np .random .random (input_shape ).astype (np .float32 )
            for _ in range (10 ):
                session .run (None ,{input_name :dummy_input })
            times =[]
            for _ in range (iterations ):
                start =time .time ()
                session .run (None ,{input_name :dummy_input })
                times .append (time .time ()-start )
        elif ext =='.h5':
            model =tf .keras .models .load_model (model_path )
            dummy_input =np .random .random (input_shape ).astype (np .float32 )
            for _ in range (10 ):
                model .predict (dummy_input ,verbose =0 )
            times =[]
            for _ in range (iterations ):
                start =time .time ()
                model .predict (dummy_input ,verbose =0 )
                times .append (time .time ()-start )
        else :
            raise ValueError (f"Неподдерживаемый формат: {ext }")
        return {
        'avg_time_ms':np .mean (times )*1000 ,
        'std_time_ms':np .std (times )*1000 ,
        'min_time_ms':np .min (times )*1000 ,
        'max_time_ms':np .max (times )*1000 ,
        'fps':1 /np .mean (times )
        }
    def get_available_optimizations (self ):
        return {
        'onnx_conversion':HAS_ONNX and HAS_TF ,
        'onnx_runtime':HAS_ONNX ,
        'tensorrt':HAS_TENSORRT ,
        'tflite':HAS_TF ,
        'fp16':True ,
        'int8_quantization':HAS_TF
        }