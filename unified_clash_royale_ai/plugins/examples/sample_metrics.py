from ..plugin_base import MetricsPlugin
from typing import Dict ,List
import time
class GameStatsPlugin (MetricsPlugin ):
    name ="Статистика игры"
    version ="1.0.0"
    author ="Столкновение Рояль ИИ"
    description ="Собирает и анализирует статистику игры"
    def __init__ (self ):
        super ().__init__ ()
        self .cards_played =0
        self .elixir_spent =0
        self .game_start_time =None
    def on_load (self ):
        print (f"Загружен плагин: {self .name }")
        self .game_start_time =time .time ()
    def on_unload (self ):
        print (f"Выгружен плагин: {self .name }")
        print (f"Статистика за сессию:")
        print (f"  Карт сыграно: {self .cards_played }")
        print (f"  Эликсира потрачено: {self .elixir_spent }")
    def get_metric_names (self )->List [str ]:
        return [
        'elixir_current',
        'elixir_advantage',
        'cards_in_hand',
        'tower_hp_ally',
        'tower_hp_enemy',
        'game_time',
        'actions_per_minute'
        ]
    def calculate_metrics (self ,game_state :Dict )->Dict :
        current_time =time .time ()
        game_duration =current_time -self .game_start_time if self .game_start_time else 0
        metrics ={
        'elixir_current':game_state .get ('our_elixir',0 ),
        'elixir_advantage':(
        game_state .get ('our_elixir',0 )-
        game_state .get ('opponent_elixir',5 )
        ),
        'cards_in_hand':len (game_state .get ('our_hand',[])),
        'tower_hp_ally':sum (
        t .get ('hp',0 )for t in game_state .get ('our_towers',[])
        ),
        'tower_hp_enemy':sum (
        t .get ('hp',0 )for t in game_state .get ('enemy_towers',[])
        ),
        'game_time':game_state .get ('game_time',0 ),
        'actions_per_minute':(
        self .cards_played /(game_duration /60 )
        if game_duration >0 else 0
        )
        }
        self .record (metrics )
        return metrics
    def on_card_played (self ,card :str ,cost :int ):
        self .cards_played +=1
        self .elixir_spent +=cost
class PerformanceMetricsPlugin (MetricsPlugin ):
    name ="Показатели производительности"
    version ="1.0.0"
    author ="Столкновение Рояль ИИ"
    description ="Мониторинг производительности"
    def __init__ (self ):
        super ().__init__ ()
        self .frame_times =[]
        self .detection_times =[]
        self .decision_times =[]
    def on_load (self ):
        print (f"Загружен плагин: {self .name }")
    def on_unload (self ):
        print (f"Выгружен плагин: {self .name }")
    def get_metric_names (self )->List [str ]:
        return [
        'fps',
        'avg_frame_time',
        'avg_detection_time',
        'avg_decision_time',
        'total_frames'
        ]
    def calculate_metrics (self ,game_state :Dict )->Dict :
        metrics ={
        'fps':self ._calculate_fps (),
        'avg_frame_time':self ._average (self .frame_times [-100 :]),
        'avg_detection_time':self ._average (self .detection_times [-100 :]),
        'avg_decision_time':self ._average (self .decision_times [-100 :]),
        'total_frames':len (self .frame_times )
        }
        self .record (metrics )
        return metrics
    def _calculate_fps (self )->float :
        if len (self .frame_times )<2 :
            return 0
        avg_time =self ._average (self .frame_times [-30 :])
        return 1 /avg_time if avg_time >0 else 0
    def _average (self ,values :List [float ])->float :
        return sum (values )/len (values )if values else 0
    def record_frame_time (self ,time_ms :float ):
        self .frame_times .append (time_ms /1000 )
    def record_detection_time (self ,time_ms :float ):
        self .detection_times .append (time_ms /1000 )
    def record_decision_time (self ,time_ms :float ):
        self .decision_times .append (time_ms /1000 )