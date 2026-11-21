import asyncio
import threading
from concurrent .futures import ThreadPoolExecutor
from queue import Queue
import time
class AsyncOperations :
    def __init__ (self ,max_workers =4 ):
        self .max_workers =max_workers
        self .executor =ThreadPoolExecutor (max_workers =max_workers )
        self .pending_tasks ={}
        self .completed_tasks ={}
        self .task_counter =0
        self .lock =threading .Lock ()
    def submit (self ,func ,*args ,callback =None ,**kwargs ):
        with self .lock :
            task_id =self .task_counter
            self .task_counter +=1
        future =self .executor .submit (func ,*args ,**kwargs )
        self .pending_tasks [task_id ]={
        'future':future ,
        'start_time':time .time (),
        'callback':callback
        }
        if callback :
            future .add_done_callback (
            lambda f :self ._on_complete (task_id ,f ,callback )
            )
        return task_id
    def _on_complete (self ,task_id ,future ,callback ):
        try :
            result =future .result ()
            callback (result )
        except Exception as e :
            callback (None ,error =e )
        finally :
            with self .lock :
                if task_id in self .pending_tasks :
                    task =self .pending_tasks .pop (task_id )
                    self .completed_tasks [task_id ]={
                    'result':future .result ()if not future .exception ()else None ,
                    'error':future .exception (),
                    'duration':time .time ()-task ['start_time']
                    }
    def get_result (self ,task_id ,timeout =None ):
        if task_id in self .completed_tasks :
            return self .completed_tasks [task_id ]['result']
        if task_id in self .pending_tasks :
            future =self .pending_tasks [task_id ]['future']
            try :
                return future .result (timeout =timeout )
            except Exception as e :
                return None
        return None
    def is_complete (self ,task_id ):
        if task_id in self .completed_tasks :
            return True
        if task_id in self .pending_tasks :
            return self .pending_tasks [task_id ]['future'].done ()
        return False
    def cancel (self ,task_id ):
        if task_id in self .pending_tasks :
            future =self .pending_tasks [task_id ]['future']
            return future .cancel ()
        return False
    def shutdown (self ,wait =True ):
        self .executor .shutdown (wait =wait )
    def get_stats (self ):
        return {
        'pending':len (self .pending_tasks ),
        'completed':len (self .completed_tasks ),
        'max_workers':self .max_workers
        }
class AsyncPipeline :
    def __init__ (self ):
        self .stages =[]
        self .is_running =False
        self .input_queue =Queue ()
        self .output_queue =Queue ()
        self .workers =[]
    def add_stage (self ,name ,func ,workers =1 ):
        self .stages .append ({
        'name':name ,
        'func':func ,
        'workers':workers ,
        'input_queue':Queue (),
        'output_queue':Queue ()
        })
    def start (self ):
        self .is_running =True
        if self .stages :
            self .stages [0 ]['input_queue']=self .input_queue
            self .stages [-1 ]['output_queue']=self .output_queue
            for i in range (len (self .stages )-1 ):
                shared_queue =Queue ()
                self .stages [i ]['output_queue']=shared_queue
                self .stages [i +1 ]['input_queue']=shared_queue
        for stage in self .stages :
            for _ in range (stage ['workers']):
                worker =threading .Thread (
                target =self ._stage_worker ,
                args =(stage ,)
                )
                worker .daemon =True
                worker .start ()
                self .workers .append (worker )
    def _stage_worker (self ,stage ):
        while self .is_running :
            try :
                item =stage ['input_queue'].get (timeout =0.1 )
                result =stage ['func'](item )
                stage ['output_queue'].put (result )
            except :
                continue
    def stop (self ):
        self .is_running =False
        for worker in self .workers :
            worker .join (timeout =1 )
    def submit (self ,item ):
        self .input_queue .put (item )
    def get_result (self ,timeout =0.1 ):
        try :
            return self .output_queue .get (timeout =timeout )
        except :
            return None
class BatchProcessor :
    def __init__ (self ,process_func ,batch_size =32 ,max_wait =0.1 ):
        self .process_func =process_func
        self .batch_size =batch_size
        self .max_wait =max_wait
        self .pending =[]
        self .pending_callbacks =[]
        self .last_batch_time =time .time ()
        self .lock =threading .Lock ()
        self .executor =ThreadPoolExecutor (max_workers =1 )
        self .is_running =True
        self .batch_thread =threading .Thread (target =self ._batch_loop )
        self .batch_thread .daemon =True
        self .batch_thread .start ()
    def submit (self ,item ,callback =None ):
        with self .lock :
            self .pending .append (item )
            self .pending_callbacks .append (callback )
    def _batch_loop (self ):
        while self .is_running :
            should_process =False
            with self .lock :
                if len (self .pending )>=self .batch_size :
                    should_process =True
                elif self .pending and time .time ()-self .last_batch_time >self .max_wait :
                    should_process =True
            if should_process :
                self ._process_batch ()
            else :
                time .sleep (0.01 )
    def _process_batch (self ):
        with self .lock :
            if not self .pending :
                return
            batch =self .pending [:self .batch_size ]
            callbacks =self .pending_callbacks [:self .batch_size ]
            self .pending =self .pending [self .batch_size :]
            self .pending_callbacks =self .pending_callbacks [self .batch_size :]
            self .last_batch_time =time .time ()
        try :
            results =self .process_func (batch )
            for i ,callback in enumerate (callbacks ):
                if callback and i <len (results ):
                    callback (results [i ])
        except Exception as e :
            print (f"Ошибка пакетной обработки: {e }")
    def shutdown (self ):
        self .is_running =False
        self .batch_thread .join (timeout =1 )
        self .executor .shutdown (wait =False )