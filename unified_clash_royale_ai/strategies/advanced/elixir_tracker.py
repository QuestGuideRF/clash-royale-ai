import time
from ...data .cards_database import get_card_info
class ElixirTracker :
    NORMAL_REGEN_RATE =2.8
    DOUBLE_ELIXIR_RATE =1.4
    TRIPLE_ELIXIR_RATE =0.9
    MAX_ELIXIR =10
    STARTING_ELIXIR =5
    def __init__ (self ):
        self .reset ()
    def reset (self ):
        self .our_elixir =self .STARTING_ELIXIR
        self .opponent_elixir =self .STARTING_ELIXIR
        self .last_update_time =time .time ()
        self .game_time =180
        self .our_card_history =[]
        self .opponent_card_history =[]
        self .current_phase ='normal'
    def update (self ,current_game_time ,detected_our_elixir =None ):
        if current_game_time <=60 :
            self .current_phase ='triple'
        elif current_game_time <=120 :
            self .current_phase ='double'
        else :
            self .current_phase ='normal'
        current_time =time .time ()
        elapsed =current_time -self .last_update_time
        self .last_update_time =current_time
        regen_rate =self ._get_regen_rate ()
        elixir_gained =elapsed /regen_rate
        self .our_elixir =min (self .MAX_ELIXIR ,self .our_elixir +elixir_gained )
        self .opponent_elixir =min (self .MAX_ELIXIR ,self .opponent_elixir +elixir_gained )
        if detected_our_elixir is not None :
            if abs (self .our_elixir -detected_our_elixir )>1 :
                self .our_elixir =detected_our_elixir
        self .game_time =current_game_time
    def _get_regen_rate (self ):
        if self .current_phase =='triple':
            return self .TRIPLE_ELIXIR_RATE
        elif self .current_phase =='double':
            return self .DOUBLE_ELIXIR_RATE
        else :
            return self .NORMAL_REGEN_RATE
    def record_our_card (self ,card_name ):
        card_info =get_card_info (card_name )
        if card_info :
            cost =card_info .get ('elixir',0 )
            self .our_elixir =max (0 ,self .our_elixir -cost )
            self .our_card_history .append ({
            'card':card_name ,
            'cost':cost ,
            'time':time .time (),
            'game_time':self .game_time
            })
    def record_opponent_card (self ,card_name ):
        card_info =get_card_info (card_name )
        if card_info :
            cost =card_info .get ('elixir',0 )
            self .opponent_elixir =max (0 ,self .opponent_elixir -cost )
            self .opponent_card_history .append ({
            'card':card_name ,
            'cost':cost ,
            'time':time .time (),
            'game_time':self .game_time
            })
    def get_our_elixir (self ):
        return int (self .our_elixir )
    def get_opponent_elixir (self ):
        return int (self .opponent_elixir )
    def get_elixir_advantage (self ):
        return self .our_elixir -self .opponent_elixir
    def can_afford (self ,card_name ):
        card_info =get_card_info (card_name )
        if card_info :
            cost =card_info .get ('elixir',0 )
            return self .our_elixir >=cost
        return False
    def time_until_afford (self ,card_name ):
        card_info =get_card_info (card_name )
        if not card_info :
            return float ('inf')
        cost =card_info .get ('elixir',0 )
        if self .our_elixir >=cost :
            return 0
        needed =cost -self .our_elixir
        return needed *self ._get_regen_rate ()
    def predict_opponent_can_afford (self ,cards ):
        affordable =[]
        for card in cards :
            card_info =get_card_info (card )
            if card_info :
                cost =card_info .get ('elixir',0 )
                if self .opponent_elixir >=cost :
                    affordable .append (card )
        return affordable
    def get_elixir_spent (self ,player ='both',last_seconds =30 ):
        cutoff =time .time ()-last_seconds
        result ={'our':0 ,'opponent':0 }
        if player in ['our','both']:
            for card in self .our_card_history :
                if card ['time']>=cutoff :
                    result ['our']+=card ['cost']
        if player in ['opponent','both']:
            for card in self .opponent_card_history :
                if card ['time']>=cutoff :
                    result ['opponent']+=card ['cost']
        return result
    def get_trade_advantage (self ,last_seconds =30 ):
        spent =self .get_elixir_spent ('both',last_seconds )
        return spent ['opponent']-spent ['our']
    def should_pressure (self ):
        advantage =self .get_elixir_advantage ()
        if advantage >=4 :
            return True ,"Большое преимущество по эликсиру, атакуйте!"
        elif advantage >=2 :
            return True ,"Небольшое преимущество, можно давить"
        elif advantage <=-3 :
            return False ,"Противник впереди по эликсиру, защищайтесь"
        else :
            return None ,"Эликсир примерно равен"
    def get_status (self ):
        return {
        'our_elixir':round (self .our_elixir ,1 ),
        'opponent_elixir':round (self .opponent_elixir ,1 ),
        'advantage':round (self .get_elixir_advantage (),1 ),
        'phase':self .current_phase ,
        'regen_rate':self ._get_regen_rate (),
        'game_time':self .game_time ,
        'our_cards_played':len (self .our_card_history ),
        'opponent_cards_played':len (self .opponent_card_history )
        }