import os
import sys
import importlib .util
from typing import Dict ,List ,Optional ,Type
from .plugin_base import PluginBase ,StrategyPlugin ,DetectorPlugin ,MetricsPlugin ,HookPlugin
class PluginManager :
    def __init__ (self ,plugins_dir :str ="plugins"):
        self .plugins_dir =plugins_dir
        self .plugins :Dict [str ,PluginBase ]={}
        self .plugin_types :Dict [str ,List [str ]]={
        'strategy':[],
        'detector':[],
        'metrics':[],
        'hook':[]
        }
        os .makedirs (plugins_dir ,exist_ok =True )
    def discover_plugins (self )->List [str ]:
        discovered =[]
        if not os .path .exists (self .plugins_dir ):
            return discovered
        for item in os .listdir (self .plugins_dir ):
            if item .endswith ('.py')and not item .startswith ('_'):
                discovered .append (item [:-3 ])
            item_path =os .path .join (self .plugins_dir ,item )
            if os .path .isdir (item_path ):
                init_path =os .path .join (item_path ,'__init__.py')
                if os .path .exists (init_path ):
                    discovered .append (item )
        return discovered
    def load_plugin (self ,plugin_name :str )->bool :
        try :
            plugin_file =os .path .join (self .plugins_dir ,f"{plugin_name }.py")
            plugin_dir =os .path .join (self .plugins_dir ,plugin_name )
            if os .path .exists (plugin_file ):
                module_path =plugin_file
            elif os .path .exists (plugin_dir ):
                module_path =os .path .join (plugin_dir ,'__init__.py')
            else :
                print (f"Плагин не найден: {plugin_name }")
                return False
            spec =importlib .util .spec_from_file_location (plugin_name ,module_path )
            module =importlib .util .module_from_spec (spec )
            sys .modules [plugin_name ]=module
            spec .loader .exec_module (module )
            plugin_class =None
            for attr_name in dir (module ):
                attr =getattr (module ,attr_name )
                if (isinstance (attr ,type )and
                issubclass (attr ,PluginBase )and
                attr is not PluginBase and
                not attr .__name__ .endswith ('Plugin')):
                    plugin_class =attr
                    break
            if plugin_class is None :
                class_name =''.join (word .capitalize ()for word in plugin_name .split ('_'))+'Plugin'
                plugin_class =getattr (module ,class_name ,None )
            if plugin_class is None :
                print (f"Класс плагина не найден в {plugin_name }")
                return False
            plugin =plugin_class ()
            plugin .on_load ()
            self .plugins [plugin_name ]=plugin
            plugin_type =getattr (plugin ,'plugin_type','unknown')
            if plugin_type in self .plugin_types :
                self .plugin_types [plugin_type ].append (plugin_name )
            print (f"Плагин загружен: {plugin .name } v{plugin .version }")
            return True
        except Exception as e :
            print (f"Ошибка загрузки плагина {plugin_name }: {e }")
            return False
    def unload_plugin (self ,plugin_name :str )->bool :
        if plugin_name not in self .plugins :
            return False
        try :
            plugin =self .plugins [plugin_name ]
            plugin .on_unload ()
            plugin_type =getattr (plugin ,'plugin_type','unknown')
            if plugin_type in self .plugin_types :
                if plugin_name in self .plugin_types [plugin_type ]:
                    self .plugin_types [plugin_type ].remove (plugin_name )
            del self .plugins [plugin_name ]
            if plugin_name in sys .modules :
                del sys .modules [plugin_name ]
            return True
        except Exception as e :
            print (f"Ошибка выгрузки плагина {plugin_name }: {e }")
            return False
    def load_all (self ):
        for plugin_name in self .discover_plugins ():
            self .load_plugin (plugin_name )
    def unload_all (self ):
        for plugin_name in list (self .plugins .keys ()):
            self .unload_plugin (plugin_name )
    def reload_plugin (self ,plugin_name :str )->bool :
        self .unload_plugin (plugin_name )
        return self .load_plugin (plugin_name )
    def get_plugin (self ,plugin_name :str )->Optional [PluginBase ]:
        return self .plugins .get (plugin_name )
    def get_plugins_by_type (self ,plugin_type :str )->List [PluginBase ]:
        plugin_names =self .plugin_types .get (plugin_type ,[])
        return [self .plugins [name ]for name in plugin_names if name in self .plugins ]
    def get_strategy_plugins (self )->List [StrategyPlugin ]:
        return self .get_plugins_by_type ('strategy')
    def get_detector_plugins (self )->List [DetectorPlugin ]:
        return self .get_plugins_by_type ('detector')
    def get_metrics_plugins (self )->List [MetricsPlugin ]:
        return self .get_plugins_by_type ('metrics')
    def get_hook_plugins (self )->List [HookPlugin ]:
        return self .get_plugins_by_type ('hook')
    def enable_plugin (self ,plugin_name :str )->bool :
        if plugin_name in self .plugins :
            self .plugins [plugin_name ].enable ()
            return True
        return False
    def disable_plugin (self ,plugin_name :str )->bool :
        if plugin_name in self .plugins :
            self .plugins [plugin_name ].disable ()
            return True
        return False
    def configure_plugin (self ,plugin_name :str ,config :Dict )->bool :
        if plugin_name in self .plugins :
            self .plugins [plugin_name ].configure (config )
            return True
        return False
    def get_all_info (self )->List [Dict ]:
        return [
        {**plugin .get_info (),'id':name }
        for name ,plugin in self .plugins .items ()
        ]
    def call_hook (self ,hook_name :str ,*args ,**kwargs ):
        for plugin in self .get_hook_plugins ():
            if plugin .enabled and hasattr (plugin ,hook_name ):
                try :
                    getattr (plugin ,hook_name )(*args ,**kwargs )
                except Exception as e :
                    print (f"Ошибка в хуке {hook_name } плагина {plugin .name }: {e }")
    def on_game_start (self ,game_state :Dict ):
        self .call_hook ('on_game_start',game_state )
    def on_game_end (self ,game_state :Dict ,result :str ):
        self .call_hook ('on_game_end',game_state ,result )
    def on_card_played (self ,card :str ,position :tuple ,is_ours :bool ):
        self .call_hook ('on_card_played',card ,position ,is_ours )
    def on_frame_processed (self ,frame ,detections :List [Dict ]):
        self .call_hook ('on_frame_processed',frame ,detections )