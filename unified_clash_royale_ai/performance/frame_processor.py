import numpy as np
import cv2
from concurrent .futures import ThreadPoolExecutor ,ProcessPoolExecutor
from queue import Queue ,Empty
import threading
import time
class FrameProcessor :
    def __init__ (self ,num_workers =4 ,use_processes =False ):
        self .num_workers =num_workers
        self .use_processes =use_processes
        self .input_queue =Queue (maxsize =30 )
        self .output_queue =Queue (maxsize =30 )
        self .is_running =False
        self .workers =[]
        self .processing_times =[]
        self .frames_processed =0
    def start (self ):
        self .is_running =True
        for i in range (self .num_workers ):
            worker =threading .Thread (target =self ._worker_loop ,args =(i ,))
            worker .daemon =True
            worker .start ()
            self .workers .append (worker )
    def stop (self ):
        self .is_running =False
        while not self .input_queue .empty ():
            try :
                self .input_queue .get_nowait ()
            except Empty :
                break
        for worker in self .workers :
            worker .join (timeout =1 )
        self .workers =[]
    def _worker_loop (self ,worker_id ):
        while self .is_running :
            try :
                task =self .input_queue .get (timeout =0.1 )
                start_time =time .time ()
                result =self ._process_frame (task )
                elapsed =time .time ()-start_time
                self .processing_times .append (elapsed )
                self .frames_processed +=1
                self .output_queue .put (result )
            except Empty :
                continue
            except Exception as e :
                print (f"Worker {worker_id } error: {e }")
    def _process_frame (self ,task ):
        frame =task ['frame']
        operations =task .get ('operations',[])
        frame_id =task .get ('frame_id',0 )
        result ={'frame_id':frame_id ,'original_shape':frame .shape }
        for op in operations :
            if op =='resize':
                frame =cv2 .resize (frame ,task .get ('size',(480 ,640 )))
                result ['resized']=frame
            elif op =='grayscale':
                gray =cv2 .cvtColor (frame ,cv2 .COLOR_BGR2GRAY )
                result ['grayscale']=gray
            elif op =='edges':
                if 'grayscale'not in result :
                    gray =cv2 .cvtColor (frame ,cv2 .COLOR_BGR2GRAY )
                else :
                    gray =result ['grayscale']
                edges =cv2 .Canny (gray ,50 ,150 )
                result ['edges']=edges
            elif op =='normalize':
                normalized =frame .astype (np .float32 )/255.0
                result ['normalized']=normalized
            elif op =='crop_cards':
                result ['cards']=self ._crop_card_regions (frame )
            elif op =='crop_battlefield':
                result ['battlefield']=self ._crop_battlefield (frame )
        result ['processed_frame']=frame
        return result
    def _crop_card_regions (self ,frame ):
        card_regions =[
        (125 ,848 ,221 ,971 ),
        (229 ,848 ,325 ,971 ),
        (333 ,848 ,429 ,971 ),
        (437 ,848 ,533 ,971 ),
        ]
        cards =[]
        for x1 ,y1 ,x2 ,y2 in card_regions :
            if y2 <=frame .shape [0 ]and x2 <=frame .shape [1 ]:
                card =frame [y1 :y2 ,x1 :x2 ]
                card =cv2 .resize (card ,(32 ,32 ))
                cards .append (card )
        return cards
    def _crop_battlefield (self ,frame ):
        y1 ,y2 =100 ,750
        x1 ,x2 =0 ,frame .shape [1 ]
        if y2 <=frame .shape [0 ]:
            return frame [y1 :y2 ,x1 :x2 ]
        return frame
    def submit_frame (self ,frame ,operations =None ,frame_id =None ):
        if operations is None :
            operations =['resize','normalize']
        task ={
        'frame':frame ,
        'operations':operations ,
        'frame_id':frame_id or self .frames_processed
        }
        try :
            self .input_queue .put_nowait (task )
            return True
        except :
            return False
    def get_result (self ,timeout =0.1 ):
        try :
            return self .output_queue .get (timeout =timeout )
        except Empty :
            return None
    def process_batch (self ,frames ,operations =None ):
        ExecutorClass =ProcessPoolExecutor if self .use_processes else ThreadPoolExecutor
        with ExecutorClass (max_workers =self .num_workers )as executor :
            tasks =[
            {'frame':f ,'operations':operations or ['resize'],'frame_id':i }
            for i ,f in enumerate (frames )
            ]
            results =list (executor .map (self ._process_frame ,tasks ))
        return results
    def get_stats (self ):
        if not self .processing_times :
            return {'fps':0 ,'avg_time':0 ,'frames_processed':0 }
        avg_time =sum (self .processing_times [-100 :])/len (self .processing_times [-100 :])
        return {
        'fps':1 /avg_time if avg_time >0 else 0 ,
        'avg_time':avg_time *1000 ,
        'frames_processed':self .frames_processed ,
        'queue_size':self .input_queue .qsize ()
        }