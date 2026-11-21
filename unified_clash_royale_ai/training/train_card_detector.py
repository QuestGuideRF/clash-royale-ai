import os
import numpy as np
import cv2
from datetime import datetime
try :
    import tensorflow as tf
    from tensorflow import keras
    from keras .models import Sequential
    from keras .layers import Conv2D ,MaxPooling2D ,Flatten ,Dense ,Dropout ,BatchNormalization
    from keras .preprocessing .image import ImageDataGenerator
    from keras .callbacks import ModelCheckpoint ,EarlyStopping ,TensorBoard
    HAS_TF =True
except ImportError :
    HAS_TF =False
class CardDetectorTrainer :
    def __init__ (self ,data_dir ="training_data/cards",model_dir ="models/card_recognition"):
        self .data_dir =data_dir
        self .model_dir =model_dir
        self .model =None
        self .history =None
        os .makedirs (model_dir ,exist_ok =True )
        os .makedirs (data_dir ,exist_ok =True )
    def build_model (self ,input_shape =(32 ,32 ,3 ),num_classes =100 ):
        if not HAS_TF :
            raise ImportError ("TensorFlow не установлен")
        model =Sequential ([
        Conv2D (32 ,(3 ,3 ),activation ='relu',padding ='same',input_shape =input_shape ),
        BatchNormalization (),
        Conv2D (32 ,(3 ,3 ),activation ='relu',padding ='same'),
        MaxPooling2D ((2 ,2 )),
        Dropout (0.25 ),
        Conv2D (64 ,(3 ,3 ),activation ='relu',padding ='same'),
        BatchNormalization (),
        Conv2D (64 ,(3 ,3 ),activation ='relu',padding ='same'),
        MaxPooling2D ((2 ,2 )),
        Dropout (0.25 ),
        Conv2D (128 ,(3 ,3 ),activation ='relu',padding ='same'),
        BatchNormalization (),
        Conv2D (128 ,(3 ,3 ),activation ='relu',padding ='same'),
        MaxPooling2D ((2 ,2 )),
        Dropout (0.25 ),
        Flatten (),
        Dense (512 ,activation ='relu'),
        BatchNormalization (),
        Dropout (0.5 ),
        Dense (256 ,activation ='relu'),
        Dropout (0.5 ),
        Dense (num_classes ,activation ='softmax')
        ])
        model .compile (
        optimizer ='adam',
        loss ='categorical_crossentropy',
        metrics =['accuracy']
        )
        self .model =model
        return model
    def prepare_data (self ,validation_split =0.2 ,batch_size =32 ):
        train_datagen =ImageDataGenerator (
        rescale =1. /255 ,
        rotation_range =10 ,
        width_shift_range =0.1 ,
        height_shift_range =0.1 ,
        shear_range =0.1 ,
        zoom_range =0.1 ,
        horizontal_flip =False ,
        validation_split =validation_split
        )
        val_datagen =ImageDataGenerator (
        rescale =1. /255 ,
        validation_split =validation_split
        )
        train_generator =train_datagen .flow_from_directory (
        self .data_dir ,
        target_size =(32 ,32 ),
        batch_size =batch_size ,
        class_mode ='categorical',
        subset ='training'
        )
        val_generator =val_datagen .flow_from_directory (
        self .data_dir ,
        target_size =(32 ,32 ),
        batch_size =batch_size ,
        class_mode ='categorical',
        subset ='validation'
        )
        return train_generator ,val_generator
    def train (self ,epochs =50 ,batch_size =32 ):
        if self .model is None :
            self .build_model ()
        train_gen ,val_gen =self .prepare_data (batch_size =batch_size )
        timestamp =datetime .now ().strftime ("%Y%m%d_%H%M%S")
        callbacks =[
        ModelCheckpoint (
        os .path .join (self .model_dir ,f'card_detector_{timestamp }_best.h5'),
        monitor ='val_accuracy',
        save_best_only =True ,
        mode ='max'
        ),
        EarlyStopping (
        monitor ='val_loss',
        patience =10 ,
        restore_best_weights =True
        ),
        TensorBoard (
        log_dir =os .path .join (self .model_dir ,'logs',timestamp )
        )
        ]
        self .history =self .model .fit (
        train_gen ,
        epochs =epochs ,
        validation_data =val_gen ,
        callbacks =callbacks
        )
        self .model .save (os .path .join (self .model_dir ,f'card_detector_{timestamp }_final.h5'))
        return self .history
    def evaluate (self ,test_dir =None ):
        if test_dir is None :
            test_dir =self .data_dir
        test_datagen =ImageDataGenerator (rescale =1. /255 )
        test_generator =test_datagen .flow_from_directory (
        test_dir ,
        target_size =(32 ,32 ),
        batch_size =32 ,
        class_mode ='categorical'
        )
        results =self .model .evaluate (test_generator )
        return {'loss':results [0 ],'accuracy':results [1 ]}
    def export_to_tflite (self ,output_path =None ):
        if output_path is None :
            output_path =os .path .join (self .model_dir ,'card_detector.tflite')
        converter =tf .lite .TFLiteConverter .from_keras_model (self .model )
        converter .optimizations =[tf .lite .Optimize .DEFAULT ]
        tflite_model =converter .convert ()
        with open (output_path ,'wb')as f :
            f .write (tflite_model )
        return output_path