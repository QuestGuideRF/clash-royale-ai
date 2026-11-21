import time
import cv2
import numpy as np
import sys
import os
sys .path .insert (0 ,os .path .dirname (os .path .dirname (os .path .abspath (__file__ ))))
from unified_clash_royale_ai .game_automation import ScreenCapture ,GameState ,ActionExecutor
from unified_clash_royale_ai .card_recognition import CardDetector
from unified_clash_royale_ai .troop_detection import TroopDetector
from unified_clash_royale_ai .rl import PDQNAgent ,ClashRoyaleEnvironment
from unified_clash_royale_ai .strategies import BotBrain ,DeckAnalyzer
from unified_clash_royale_ai .utils import Logger ,MatchRecorder ,Statistics
from unified_clash_royale_ai .config import *
class UnifiedClashRoyaleAI :
    def __init__ (self ,use_rl =True ,use_card_detection =True ,use_troop_detection =True ,use_gui =False ):
        self .use_rl =use_rl
        self .use_card_detection =use_card_detection
        self .use_troop_detection =use_troop_detection
        self .use_gui =use_gui
        self .running =False
        self .logger =Logger ()
        self .statistics =Statistics ()
        self .match_recorder =MatchRecorder ()
        self .logger .info ("="*60 )
        self .logger .info ("🎮 ЕДИНЫЙ ИИ CLASH ROYALE v1.0")
        self .logger .info ("="*60 )
        self .logger .info ("Инициализация компонентов...")
        try :
            self .screen_capture =ScreenCapture ()
            window_coords =self .screen_capture .get_window_coords ()
            self .logger .info ("✓ Модуль захвата экрана загружен")
        except Exception as e :
            self .logger .error (f"✗ Ошибка модуля захвата экрана: {e }")
            self .screen_capture =None
            window_coords =(0 ,0 )
        self .game_state =GameState ()
        self .logger .info ("✓ Модуль состояния игры загружен")
        self .action_executor =ActionExecutor (window_coords )
        self .logger .info ("✓ Модуль исполнения действий загружен")
        self .deck_analyzer =DeckAnalyzer ()
        self .logger .info ("✓ Анализатор колод загружен")
        self .bot_brain =BotBrain (self .game_state ,self .action_executor )
        self .logger .info ("✓ Мозг бота загружен")
        if use_card_detection :
            try :
                self .card_detector =CardDetector ()
                self .logger .info ("✓ Модуль распознавания карт загружен")
            except Exception as e :
                self .logger .warning (f"⚠ Ошибка модуля распознавания карт: {e }")
                self .card_detector =None
        else :
            self .card_detector =None
        if use_troop_detection :
            try :
                self .troop_detector =TroopDetector ()
                self .logger .info ("✓ Модуль обнаружения войск загружен")
            except Exception as e :
                self .logger .warning (f"⚠ Ошибка модуля обнаружения войск: {e }")
                self .troop_detector =None
        else :
            self .troop_detector =None
        if use_rl :
            try :
                self .env =ClashRoyaleEnvironment (
                self .screen_capture ,
                self .game_state ,
                self .action_executor
                )
                self .rl_agent =PDQNAgent (self .env )
                self .logger .info ("✓ Модуль Reinforcement Learning загружен")
            except Exception as e :
                self .logger .warning (f"⚠ Ошибка модуля RL: {e }")
                self .rl_agent =None
                self .env =None
        else :
            self .rl_agent =None
            self .env =None
        self .gui =None
        if use_gui :
            try :
                from unified_clash_royale_ai .gui import ClashRoyaleGUI
                self .gui =ClashRoyaleGUI (self )
                self .logger .info ("✓ GUI загружен")
            except Exception as e :
                self .logger .warning (f"⚠ Ошибка загрузки GUI: {e }")
        self .logger .info ("="*60 )
        self .logger .info ("Инициализация завершена!")
        self .logger .info ("="*60 )
    def run_smart_bot (self ,screenshot ,enemy_troops ,ally_troops ):
        action =self .bot_brain .decide_action (enemy_troops ,ally_troops )
        if action :
            card_index ,position =action
            card =self .game_state .cards_in_hand .get (card_index )
            if card :
                self .logger .action (card ,position ,self .game_state .elixir_blue )
                self .statistics .record_card_played (card )
                self .bot_brain .execute_action (action )
    def run_rl_agent (self ,screenshot ):
        if self .rl_agent is None or self .env is None :
            return
        processed_image =self .screen_capture .process_image (screenshot )
        state =self .env .get_state (processed_image )
        action =self .rl_agent .make_action (state ,step =0 )
        self .env .step (action )
    def update_gui (self ,fps ):
        if self .gui :
            self .gui .update_opponent_hand (self .card_detector .get_opponent_hand ()if self .card_detector else [])
            self .gui .update_elixir (self .game_state .elixir_blue )
            self .gui .update_towers (self .game_state .towers_blue ,self .game_state .towers_red )
            self .gui .update_timer (self .game_state .chrono )
            self .gui .update_fps (fps )
    def run (self ,mode ='hybrid'):
        self .running =True
        self .logger .info (f"🚀 Запуск AI в режиме: {mode }")
        self .logger .match_start ()
        match_id =self .match_recorder .start_recording ()
        self .logger .info (f"📹 Запись матча: {match_id }")
        frame_count =0
        fps_start_time =time .time ()
        current_fps =0
        while self .running :
            try :
                loop_start =time .time ()
                if self .screen_capture is None :
                    time .sleep (0.1 )
                    continue
                screenshot =self .screen_capture .take_screenshot ()
                self .game_state .update_timer ()
                enemy_troops ={'all':([],[]),'left':([],[]),'right':([],[])}
                ally_troops ={'all':([],[]),'left':([],[]),'right':([],[])}
                if self .troop_detector :
                    detections ,_ =self .troop_detector .detect_troops (screenshot )
                    if detections :
                        enemy_troops ,ally_troops =self .troop_detector .categorize_troops (
                        detections ,screenshot .shape [0 ]
                        )
                if self .card_detector :
                    pass
                self .match_recorder .record_frame (screenshot ,time .time ())
                if mode =='rl':
                    self .run_rl_agent (screenshot )
                elif mode =='rule_based':
                    self .run_smart_bot (screenshot ,enemy_troops ,ally_troops )
                elif mode =='smart':
                    self .run_smart_bot (screenshot ,enemy_troops ,ally_troops )
                elif mode =='hybrid':
                    if self .rl_agent and np .random .random ()<0.3 :
                        self .run_rl_agent (screenshot )
                    else :
                        self .run_smart_bot (screenshot ,enemy_troops ,ally_troops )
                frame_count +=1
                if time .time ()-fps_start_time >=1 :
                    current_fps =frame_count /(time .time ()-fps_start_time )
                    fps_start_time =time .time ()
                    frame_count =0
                if self .gui :
                    self .update_gui (current_fps )
                elapsed =time .time ()-loop_start
                if elapsed <0.1 :
                    time .sleep (0.1 -elapsed )
            except KeyboardInterrupt :
                self .logger .info ("\n⏹️ Остановка AI по запросу пользователя...")
                break
            except Exception as e :
                self .logger .error (f"Ошибка в главном цикле: {e }")
                time .sleep (1 )
        self .match_recorder .stop_recording ()
        self .logger .match_end ("unknown",self .game_state .towers_red ,self .game_state .towers_blue )
        self .statistics .print_summary ()
    def stop (self ):
        self .running =False
def main ():
    import argparse
    parser =argparse .ArgumentParser (description ='🎮 Единый искусственный интеллект Clash Royale')
    parser .add_argument ('--mode',choices =['rl','rule_based','hybrid','smart'],
    default ='smart',help ='Режим работы AI')
    parser .add_argument ('--no-rl',action ='store_true',
    help ='Отключить reinforcement learning')
    parser .add_argument ('--no-cards',action ='store_true',
    help ='Отключить распознавание карт')
    parser .add_argument ('--no-troops',action ='store_true',
    help ='Отключить обнаружение войск')
    parser .add_argument ('--gui',action ='store_true',
    help ='Включить графический интерфейс')
    parser .add_argument ('--stats',action ='store_true',
    help ='Показать статистику и выйти')
    args =parser .parse_args ()
    if args .stats :
        stats =Statistics ()
        stats .print_summary ()
        return
    ai =UnifiedClashRoyaleAI (
    use_rl =not args .no_rl ,
    use_card_detection =not args .no_cards ,
    use_troop_detection =not args .no_troops ,
    use_gui =args .gui
    )
    if args .gui and ai .gui :
        ai .gui .run ()
    else :
        ai .run (mode =args .mode )
if __name__ =="__main__":
    main ()