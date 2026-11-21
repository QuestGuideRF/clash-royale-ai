from collections import deque
class CycleCounter :
    DECK_SIZE =8
    HAND_SIZE =4
    def __init__ (self ):
        self .reset ()
    def reset (self ):
        self .our_deck =[]
        self .our_hand =[]
        self .our_next_card =None
        self .our_played_history =deque (maxlen =100 )
        self .opponent_seen_cards =[]
        self .opponent_played_history =deque (maxlen =100 )
        self .opponent_cycle_position ={}
    def set_our_deck (self ,deck ):
        self .our_deck =list (deck )
        self .our_hand =deck [:4 ]
        self .our_next_card =deck [4 ]if len (deck )>4 else None
    def record_our_play (self ,card ):
        if card in self .our_hand :
            self .our_hand .remove (card )
            self .our_played_history .append (card )
            if self .our_next_card :
                self .our_hand .append (self .our_next_card )
            self ._update_next_card ()
    def _update_next_card (self ):
        cards_not_in_hand =[c for c in self .our_deck if c not in self .our_hand ]
        if cards_not_in_hand and self .our_played_history :
            for card in self .our_played_history :
                if card in cards_not_in_hand :
                    self .our_next_card =card
                    break
    def record_opponent_play (self ,card ):
        self .opponent_played_history .append (card )
        if card not in self .opponent_seen_cards :
            self .opponent_seen_cards .append (card )
        for existing_card in self .opponent_cycle_position :
            self .opponent_cycle_position [existing_card ]+=1
        self .opponent_cycle_position [card ]=0
    def get_our_hand (self ):
        return list (self .our_hand )
    def get_our_next_card (self ):
        return self .our_next_card
    def cards_until (self ,card ):
        if card in self .our_hand :
            return 0
        if card ==self .our_next_card :
            return 1
        cards_in_cycle =[c for c in self .our_deck if c not in self .our_hand and c !=self .our_next_card ]
        for i ,c in enumerate (cards_in_cycle ):
            if c ==card :
                return i +2
        return self .DECK_SIZE
    def get_opponent_seen_cards (self ):
        return list (self .opponent_seen_cards )
    def get_opponent_unseen_count (self ):
        return self .DECK_SIZE -len (self .opponent_seen_cards )
    def predict_opponent_hand (self ):
        if not self .opponent_seen_cards :
            return []
        hand_predictions =[]
        for card in self .opponent_seen_cards :
            position =self .opponent_cycle_position .get (card ,0 )
            in_hand_probability =min (1.0 ,position /4.0 )
            hand_predictions .append ({
            'card':card ,
            'in_hand_probability':in_hand_probability ,
            'cycle_position':position
            })
        hand_predictions .sort (key =lambda x :x ['in_hand_probability'],reverse =True )
        return hand_predictions
    def is_card_in_opponent_hand (self ,card ,threshold =0.5 ):
        if card not in self .opponent_seen_cards :
            return None
        position =self .opponent_cycle_position .get (card ,0 )
        probability =min (1.0 ,position /4.0 )
        return probability >=threshold
    def get_opponent_cycle_info (self ):
        return {
        'seen_cards':len (self .opponent_seen_cards ),
        'unseen_cards':self .get_opponent_unseen_count (),
        'total_plays':len (self .opponent_played_history ),
        'predicted_hand':self .predict_opponent_hand ()[:4 ]
        }
    def get_key_card_status (self ,key_cards ):
        status ={}
        for card in key_cards :
            if card in self .opponent_seen_cards :
                position =self .opponent_cycle_position .get (card ,0 )
                status [card ]={
                'seen':True ,
                'likely_in_hand':position >=4 ,
                'cards_since_played':position
                }
            else :
                status [card ]={
                'seen':False ,
                'likely_in_hand':None ,
                'cards_since_played':None
                }
        return status
    def should_we_play_first (self ,card ,opponent_counter ):
        counter_in_hand =self .is_card_in_opponent_hand (opponent_counter )
        if counter_in_hand is None :
            return None ,"Контр-карта еще не была замечена"
        elif counter_in_hand :
            return False ,f"Вероятно {opponent_counter } в руке противника, подождите"
        else :
            return True ,f"{opponent_counter } скорее всего не в руке, можно играть"
    def get_full_report (self ):
        our_info ={
        'deck':self .our_deck ,
        'hand':self .our_hand ,
        'next_card':self .our_next_card ,
        'total_plays':len (self .our_played_history )
        }
        opponent_info =self .get_opponent_cycle_info ()
        return {
        'our':our_info ,
        'opponent':opponent_info
        }