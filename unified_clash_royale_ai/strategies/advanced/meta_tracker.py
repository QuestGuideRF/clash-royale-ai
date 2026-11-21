import json
import os
from datetime import datetime ,timedelta
from collections import defaultdict
class MetaTracker :
    def __init__ (self ,data_file ="data/meta_data.json"):
        self .data_file =data_file
        self .meta_data =self ._load_data ()
    def _load_data (self ):
        if os .path .exists (self .data_file ):
            with open (self .data_file ,'r')as f :
                return json .load (f )
        return {
        'cards':{},
        'decks':{},
        'archetypes':{},
        'last_updated':None
        }
    def _save_data (self ):
        os .makedirs (os .path .dirname (self .data_file )or '.',exist_ok =True )
        with open (self .data_file ,'w')as f :
            json .dump (self .meta_data ,f ,indent =2 )
    def record_match (self ,deck ,opponent_deck ,result ,trophy_range =None ):
        timestamp =datetime .now ().isoformat ()
        for card in opponent_deck :
            if card not in self .meta_data ['cards']:
                self .meta_data ['cards'][card ]={
                'appearances':0 ,
                'wins_against':0 ,
                'losses_against':0 ,
                'last_seen':None
                }
            self .meta_data ['cards'][card ]['appearances']+=1
            self .meta_data ['cards'][card ]['last_seen']=timestamp
            if result =='win':
                self .meta_data ['cards'][card ]['wins_against']+=1
            elif result =='loss':
                self .meta_data ['cards'][card ]['losses_against']+=1
        deck_key =','.join (sorted (opponent_deck ))
        if deck_key not in self .meta_data ['decks']:
            self .meta_data ['decks'][deck_key ]={
            'appearances':0 ,
            'wins_against':0 ,
            'losses_against':0 ,
            'cards':opponent_deck
            }
        self .meta_data ['decks'][deck_key ]['appearances']+=1
        if result =='win':
            self .meta_data ['decks'][deck_key ]['wins_against']+=1
        elif result =='loss':
            self .meta_data ['decks'][deck_key ]['losses_against']+=1
        self .meta_data ['last_updated']=timestamp
        self ._save_data ()
    def get_popular_cards (self ,limit =20 ):
        cards =self .meta_data ['cards']
        sorted_cards =sorted (
        cards .items (),
        key =lambda x :x [1 ]['appearances'],
        reverse =True
        )
        return [
        {
        'card':card ,
        'usage_rate':data ['appearances'],
        'win_rate_against':self ._calc_win_rate (data )
        }
        for card ,data in sorted_cards [:limit ]
        ]
    def get_popular_decks (self ,limit =10 ):
        decks =self .meta_data ['decks']
        sorted_decks =sorted (
        decks .items (),
        key =lambda x :x [1 ]['appearances'],
        reverse =True
        )
        return [
        {
        'cards':data ['cards'],
        'appearances':data ['appearances'],
        'win_rate_against':self ._calc_win_rate (data )
        }
        for _ ,data in sorted_decks [:limit ]
        ]
    def _calc_win_rate (self ,data ):
        total =data .get ('wins_against',0 )+data .get ('losses_against',0 )
        if total ==0 :
            return 0.5
        return data .get ('wins_against',0 )/total
    def get_card_trends (self ,days =7 ):
        cutoff =(datetime .now ()-timedelta (days =days )).isoformat ()
        trends ={}
        for card ,data in self .meta_data ['cards'].items ():
            if data .get ('last_seen')and data ['last_seen']>cutoff :
                trends [card ]={
                'recent_appearances':data ['appearances'],
                'trending':True
                }
        return dict (sorted (trends .items (),key =lambda x :x [1 ]['recent_appearances'],reverse =True ))
    def predict_opponent_deck (self ,seen_cards ):
        if len (seen_cards )<2 :
            return None
        best_match =None
        best_score =0
        for deck_key ,data in self .meta_data ['decks'].items ():
            deck_cards =set (data ['cards'])
            match_count =len (set (seen_cards )&deck_cards )
            if match_count >best_score :
                best_score =match_count
                best_match =data
        if best_match and best_score >=len (seen_cards )*0.5 :
            return {
            'predicted_deck':best_match ['cards'],
            'confidence':best_score /len (seen_cards ),
            'remaining_cards':list (set (best_match ['cards'])-set (seen_cards ))
            }
        return None
    def get_counter_recommendations (self ,opponent_cards ):
        from ...data .cards_database import get_counter_cards
        recommendations =[]
        for card in opponent_cards :
            counters =get_counter_cards (card )
            for counter in counters :
                recommendations .append ({
                'counter':counter ,
                'against':card
                })
        return recommendations
    def get_meta_report (self ):
        total_matches =sum (d ['appearances']for d in self .meta_data ['decks'].values ())
        report ={
        'total_matches_tracked':total_matches ,
        'unique_cards_seen':len (self .meta_data ['cards']),
        'unique_decks_seen':len (self .meta_data ['decks']),
        'top_cards':self .get_popular_cards (10 ),
        'top_decks':self .get_popular_decks (5 ),
        'last_updated':self .meta_data .get ('last_updated')
        }
        return report
    def import_royale_api_data (self ,api_data ):
        if 'cards'in api_data :
            for card in api_data ['cards']:
                card_name =card .get ('name','').lower ().replace (' ','_')
                self .meta_data ['cards'][card_name ]={
                'appearances':card .get ('usage',0 ),
                'wins_against':0 ,
                'losses_against':0 ,
                'api_win_rate':card .get ('win_rate',0.5 )
                }
        self ._save_data ()