from abc import ABC ,abstractmethod
from typing import Any ,Dict ,List ,Optional
class PluginBase (ABC ):
    name :str ="Безымянный плагин"
    version :str ="1.0.0"
    author :str ="Unknown"
    description :str =""
    def __init__ (self ):
        self .enabled =True
        self .config ={}
    @abstractmethod
    def on_load (self ):
        pass
    @abstractmethod
    def on_unload (self ):
        pass
    def get_info (self )->Dict :
        return {
        'name':self .name ,
        'version':self .version ,
        'author':self .author ,
        'description':self .description ,
        'enabled':self .enabled
        }
    def configure (self ,config :Dict ):
        self .config .update (config )
    def enable (self ):
        self .enabled =True
    def disable (self ):
        self .enabled =False
class StrategyPlugin (PluginBase ):
    plugin_type ="strategy"
    @abstractmethod
    def decide_action (self ,game_state :Dict )->Optional [Dict ]:
        pass
    @abstractmethod
    def get_priority (self )->int :
        pass
    def should_activate (self ,game_state :Dict )->bool :
        return True
    def on_action_executed (self ,action :Dict ,result :Dict ):
        pass
class DetectorPlugin (PluginBase ):
    plugin_type ="detector"
    @abstractmethod
    def detect (self ,frame )->List [Dict ]:
        pass
    @abstractmethod
    def get_detection_types (self )->List [str ]:
        pass
    def preprocess (self ,frame ):
        return frame
    def postprocess (self ,detections :List [Dict ])->List [Dict ]:
        return detections
class MetricsPlugin (PluginBase ):
    plugin_type ="metrics"
    def __init__ (self ):
        super ().__init__ ()
        self .metrics_history =[]
    @abstractmethod
    def calculate_metrics (self ,game_state :Dict )->Dict :
        pass
    @abstractmethod
    def get_metric_names (self )->List [str ]:
        pass
    def record (self ,metrics :Dict ):
        self .metrics_history .append (metrics )
    def get_history (self )->List [Dict ]:
        return self .metrics_history
    def clear_history (self ):
        self .metrics_history =[]
    def get_summary (self )->Dict :
        if not self .metrics_history :
            return {}
        summary ={}
        metric_names =self .get_metric_names ()
        for name in metric_names :
            values =[m .get (name ,0 )for m in self .metrics_history if name in m ]
            if values :
                summary [name ]={
                'count':len (values ),
                'sum':sum (values ),
                'avg':sum (values )/len (values ),
                'min':min (values ),
                'max':max (values )
                }
        return summary
class HookPlugin (PluginBase ):
    plugin_type ="hook"
    def on_game_start (self ,game_state :Dict ):
        pass
    def on_game_end (self ,game_state :Dict ,result :str ):
        pass
    def on_card_played (self ,card :str ,position :tuple ,is_ours :bool ):
        pass
    def on_tower_destroyed (self ,tower :str ,is_ours :bool ):
        pass
    def on_elixir_change (self ,old_value :int ,new_value :int ):
        pass
    def on_frame_processed (self ,frame ,detections :List [Dict ]):
        pass