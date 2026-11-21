import time
import logging
import traceback
import sys
import os
from typing import Callable ,Optional ,Dict
from datetime import datetime
import threading
class AutoRestart :
    def __init__ (self ,max_restarts :int =5 ,
    restart_delay :float =5.0 ,
    cooldown_period :float =300.0 ,
    log_file :str ="logs/restart.log"):
        self .max_restarts =max_restarts
        self .restart_delay =restart_delay
        self .cooldown_period =cooldown_period
        self .log_file =log_file
        self .restart_count =0
        self .restart_history =[]
        self .is_running =False
        self .should_restart =True
        self .last_restart_time =None
        os .makedirs (os .path .dirname (log_file )or '.',exist_ok =True )
        logging .basicConfig (
        filename =log_file ,
        level =logging .INFO ,
        format ='%(asctime)s - %(имя уровня)s - %(сообщение)s'
        )
        self .logger =logging .getLogger (__name__ )
    def reset_counter (self ):
        current_time =time .time ()
        self .restart_history =[
        t for t in self .restart_history
        if current_time -t <self .cooldown_period
        ]
        self .restart_count =len (self .restart_history )
    def can_restart (self )->bool :
        self .reset_counter ()
        return self .restart_count <self .max_restarts
    def register_restart (self ):
        current_time =time .time ()
        self .restart_history .append (current_time )
        self .last_restart_time =current_time
        self .restart_count =len (self .restart_history )
    def handle_crash (self ,exception :Exception ,context :str =""):
        error_msg =f"Краш обнаружен: {type (exception ).__name__ }: {str (exception )}"
        if context :
            error_msg +=f" | Контекст: {context }"
        self .logger .error (error_msg )
        self .logger .error (traceback .format_exc ())
        print (f"\n❌ {error_msg }")
        print (f"📋 Traceback сохранен в {self .log_file }")
        if self .can_restart ():
            print (f"\n🔄 Автоматический перезапуск через {self .restart_delay } секунд...")
            print (f"📊 Перезапусков в последний час: {self .restart_count }/{self .max_restarts }")
            self .register_restart ()
            time .sleep (self .restart_delay )
            return True
        else :
            print (f"\n⚠️ Достигнут лимит перезапусков ({self .max_restarts })")
            print (f"⏸️ Перезапуск отложен на {self .cooldown_period /60 :.1f} минут")
            return False
    def run_with_restart (self ,func :Callable ,*args ,**kwargs ):
        self .is_running =True
        self .should_restart =True
        while self .should_restart and self .can_restart ():
            try :
                print (f"\n🚀 Запуск... (попытка {self .restart_count +1 })")
                func (*args ,**kwargs )
                self .should_restart =False
            except KeyboardInterrupt :
                print ("\n⚠️ Прервано пользователем")
                self .should_restart =False
                break
            except SystemExit :
                print ("\n👋 Выход")
                self .should_restart =False
                break
            except Exception as e :
                if not self .handle_crash (e ,func .__name__ ):
                    self .should_restart =False
                    raise
        self .is_running =False
    def stop (self ):
        self .should_restart =False
        self .logger .info ("Авто-перезапуск остановлен")
    def get_status (self )->Dict :
        self .reset_counter ()
        return {
        'is_running':self .is_running ,
        'restart_count':self .restart_count ,
        'max_restarts':self .max_restarts ,
        'can_restart':self .can_restart (),
        'last_restart_time':(
        datetime .fromtimestamp (self .last_restart_time ).isoformat ()
        if self .last_restart_time else None
        ),
        'restarts_remaining':max (0 ,self .max_restarts -self .restart_count )
        }
class HealthMonitor :
    def __init__ (self ,check_interval :float =30.0 ,
    max_failures :int =3 ):
        self .check_interval =check_interval
        self .max_failures =max_failures
        self .failure_count =0
        self .last_check_time =time .time ()
        self .is_monitoring =False
        self .monitor_thread =None
        self .health_checks =[]
    def add_health_check (self ,check_func :Callable [[],bool ],name :str =""):
        self .health_checks .append ({
        'func':check_func ,
        'name':name or check_func .__name__
        })
    def check_health (self )->bool :
        all_ok =True
        for check in self .health_checks :
            try :
                if not check ['func']():
                    print (f"⚠️ Проверка не пройдена: {check ['name']}")
                    all_ok =False
            except Exception as e :
                print (f"❌ Ошибка проверки {check ['name']}: {e }")
                all_ok =False
        return all_ok
    def start_monitoring (self ,on_failure :Callable ):
        if self .is_monitoring :
            return
        self .is_monitoring =True
        self .monitor_thread =threading .Thread (
        target =self ._monitor_loop ,
        args =(on_failure ,),
        daemon =True
        )
        self .monitor_thread .start ()
    def _monitor_loop (self ,on_failure :Callable ):
        while self .is_monitoring :
            time .sleep (self .check_interval )
            if not self .check_health ():
                self .failure_count +=1
                print (f"⚠️ Проблема обнаружена ({self .failure_count }/{self .max_failures })")
                if self .failure_count >=self .max_failures :
                    print ("🔄 Превышен лимит неудач, требуется перезапуск")
                    on_failure ()
                    self .failure_count =0
            else :
                if self .failure_count >0 :
                    self .failure_count =0
    def stop_monitoring (self ):
        self .is_monitoring =False
        if self .monitor_thread :
            self .monitor_thread .join (timeout =1 )
class Watchdog :
    def __init__ (self ,max_restarts :int =5 ,
    restart_delay :float =5.0 ,
    health_check_interval :float =30.0 ):
        self .auto_restart =AutoRestart (
        max_restarts =max_restarts ,
        restart_delay =restart_delay
        )
        self .health_monitor =HealthMonitor (
        check_interval =health_check_interval ,
        max_failures =3
        )
    def add_health_check (self ,check_func :Callable [[],bool ],name :str =""):
        self .health_monitor .add_health_check (check_func ,name )
    def run (self ,main_func :Callable ,*args ,**kwargs ):
        def on_health_failure ():
            exception =Exception ("Проверка работоспособности не удалась")
            self .auto_restart .handle_crash (exception ,"Монитор здоровья")
        self .health_monitor .start_monitoring (on_health_failure )
        try :
            self .auto_restart .run_with_restart (main_func ,*args ,**kwargs )
        finally :
            self .health_monitor .stop_monitoring ()
    def get_status (self )->Dict :
        return {
        'auto_restart':self .auto_restart .get_status (),
        'health_monitor':{
        'is_monitoring':self .health_monitor .is_monitoring ,
        'failure_count':self .health_monitor .failure_count ,
        'health_checks_count':len (self .health_monitor .health_checks )
        }
        }