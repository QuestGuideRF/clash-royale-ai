import os
import logging
from datetime import datetime
class Logger :
    def __init__ (self ,name ="ClashRoyaleAI",log_dir ="logs"):
        self .name =name
        self .log_dir =log_dir
        os .makedirs (log_dir ,exist_ok =True )
        self .logger =logging .getLogger (name )
        self .logger .setLevel (logging .DEBUG )
        formatter =logging .Formatter (
        '%(asctime)s | %(имя уровня)-8s | %(сообщение)с',
        datefmt ='%Y-%m-%d %H:%M:%S'
        )
        log_file =os .path .join (
        log_dir ,
        f"clash_ai_{datetime .now ().strftime ('%Y%m%d_%H%M%S')}.log"
        )
        file_handler =logging .FileHandler (log_file ,encoding ='utf-8')
        file_handler .setLevel (logging .DEBUG )
        file_handler .setFormatter (formatter )
        console_handler =logging .StreamHandler ()
        console_handler .setLevel (logging .INFO )
        console_handler .setFormatter (formatter )
        self .logger .addHandler (file_handler )
        self .logger .addHandler (console_handler )
    def debug (self ,message ):
        self .logger .debug (message )
    def info (self ,message ):
        self .logger .info (message )
    def warning (self ,message ):
        self .logger .warning (message )
    def error (self ,message ):
        self .logger .error (message )
    def critical (self ,message ):
        self .logger .critical (message )
    def action (self ,card ,position ,elixir ):
        self .info (f"ACTION: Played {card } at {position } (Elixir: {elixir })")
    def game_event (self ,event_type ,details ):
        self .info (f"EVENT: {event_type } - {details }")
    def match_start (self ):
        self .info ("="*50 )
        self .info ("МАТЧ НАЧАЛСЯ")
        self .info ("="*50 )
    def match_end (self ,result ,crowns_player ,crowns_enemy ):
        self .info ("="*50 )
        self .info (f"MATCH ENDED: {result }")
        self .info (f"Score: {crowns_player } - {crowns_enemy }")
        self .info ("="*50 )