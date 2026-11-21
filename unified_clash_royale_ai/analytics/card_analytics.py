import json
import os
from typing import Dict ,List ,Optional
from datetime import datetime
from collections import defaultdict
class CardAnalytics :
    def __init__ (self ,data_file :str ="data/card_analytics.json"):
        self .data_file =data_file
        self .data =self ._load_data ()
    def _load_data (self )->Dict :
        if os .path .exists (self .data_file ):
            with open (self .data_file ,'r',encoding ='utf-8')as f :
                return json .load (f )
        return {
        'cards':{},
        'matchups':{},
        'placements':{},
        'combos':{}
        }
    def _save_data (self ):
        os .makedirs (os .path .dirname (self .data_file )or '.',exist_ok =True )
        with open (self .data_file ,'w',encoding ='utf-8')as f :
            json .dump (self .data ,f ,indent =2 ,ensure_ascii =False )
    def record_card_play (self ,card :str ,elixir :int ,position :tuple ,
    result :str ,game_time :int ,opponent_cards :List [str ]=None ):
        if card not in self .data ['cards']:
            self .data ['cards'][card ]={
            'plays':0 ,
            'wins':0 ,
            'losses':0 ,
            'draws':0 ,
            'total_elixir':0 ,
            'positions':defaultdict (int ),
            'time_distribution':defaultdict (int )
            }
        card_data =self .data ['cards'][card ]
        card_data ['plays']+=1
        card_data ['total_elixir']+=elixir
        if result =='win':
            card_data ['wins']+=1
        elif result =='loss':
            card_data ['losses']+=1
        else :
            card_data ['draws']+=1
        pos_key =f"{int (position [0 ]//50 )*50 },{int (position [1 ]//50 )*50 }"
        card_data ['positions'][pos_key ]=card_data ['positions'].get (pos_key ,0 )+1
        time_bucket =(game_time //30 )*30
        card_data ['time_distribution'][str (time_bucket )]=card_data ['time_distribution'].get (str (time_bucket ),0 )+1
        if opponent_cards :
            for opp_card in opponent_cards :
                matchup_key =f"{card }_{opp_card }"
                if matchup_key not in self .data ['matchups']:
                    self .data ['matchups'][matchup_key ]={
                    'encounters':0 ,
                    'wins':0 ,
                    'losses':0
                    }
                self .data ['matchups'][matchup_key ]['encounters']+=1
                if result =='win':
                    self .data ['matchups'][matchup_key ]['wins']+=1
                elif result =='loss':
                    self .data ['matchups'][matchup_key ]['losses']+=1
        self ._save_data ()
    def record_combo (self ,cards :List [str ],result :str ):
        combo_key ='_'.join (sorted (cards ))
        if combo_key not in self .data ['combos']:
            self .data ['combos'][combo_key ]={
            'cards':cards ,
            'plays':0 ,
            'wins':0 ,
            'losses':0
            }
        self .data ['combos'][combo_key ]['plays']+=1
        if result =='win':
            self .data ['combos'][combo_key ]['wins']+=1
        elif result =='loss':
            self .data ['combos'][combo_key ]['losses']+=1
        self ._save_data ()
    def get_card_stats (self ,card :str )->Dict :
        if card not in self .data ['cards']:
            return None
        card_data =self .data ['cards'][card ]
        total_games =card_data ['wins']+card_data ['losses']+card_data ['draws']
        return {
        'card':card ,
        'plays':card_data ['plays'],
        'total_games':total_games ,
        'win_rate':card_data ['wins']/total_games if total_games >0 else 0 ,
        'avg_elixir_per_play':(
        card_data ['total_elixir']/card_data ['plays']
        if card_data ['plays']>0 else 0
        ),
        'most_common_position':(
        max (card_data ['positions'],key =card_data ['positions'].get )
        if card_data ['positions']else None
        ),
        'best_time_to_play':self ._get_best_time (card_data ['time_distribution'])
        }
    def _get_best_time (self ,time_distribution :Dict )->Optional [str ]:
        if not time_distribution :
            return None
        best_time =max (time_distribution ,key =time_distribution .get )
        seconds =int (best_time )
        minutes =seconds //60
        secs =seconds %60
        return f"{minutes }:{secs :02d}"
    def get_card_matchups (self ,card :str )->List [Dict ]:
        matchups =[]
        for key ,data in self .data ['matchups'].items ():
            if key .startswith (f"{card }_"):
                opponent_card =key .replace (f"{card }_","")
                total =data ['wins']+data ['losses']
                matchups .append ({
                'opponent_card':opponent_card ,
                'encounters':data ['encounters'],
                'win_rate':data ['wins']/total if total >0 else 0.5
                })
        matchups .sort (key =lambda x :x ['win_rate'],reverse =True )
        return matchups
    def get_best_combos (self ,limit :int =10 )->List [Dict ]:
        combos =[]
        for key ,data in self .data ['combos'].items ():
            total =data ['wins']+data ['losses']
            if total >=5 :
                combos .append ({
                'cards':data ['cards'],
                'plays':data ['plays'],
                'win_rate':data ['wins']/total if total >0 else 0.5
                })
        combos .sort (key =lambda x :x ['win_rate'],reverse =True )
        return combos [:limit ]
    def get_overall_stats (self )->Dict :
        total_plays =sum (c ['plays']for c in self .data ['cards'].values ())
        total_wins =sum (c ['wins']for c in self .data ['cards'].values ())
        total_losses =sum (c ['losses']for c in self .data ['cards'].values ())
        most_played =max (
        self .data ['cards'].items (),
        key =lambda x :x [1 ]['plays']
        )if self .data ['cards']else (None ,None )
        highest_winrate =None
        if self .data ['cards']:
            for card ,data in self .data ['cards'].items ():
                total =data ['wins']+data ['losses']
                if total >=10 :
                    wr =data ['wins']/total
                    if highest_winrate is None or wr >highest_winrate [1 ]:
                        highest_winrate =(card ,wr )
        return {
        'total_card_plays':total_plays ,
        'total_matches':total_wins +total_losses ,
        'overall_win_rate':(
        total_wins /(total_wins +total_losses )
        if (total_wins +total_losses )>0 else 0
        ),
        'unique_cards_used':len (self .data ['cards']),
        'most_played_card':most_played [0 ]if most_played [0 ]else None ,
        'highest_winrate_card':highest_winrate [0 ]if highest_winrate else None
        }
    def generate_report (self )->str :
        stats =self .get_overall_stats ()
        report =[]
        report .append ("="*60 )
        report .append ("АНАЛИТИКА КАРТ")
        report .append ("="*60 )
        report .append (f"\nВсего игр: {stats ['total_matches']}")
        report .append (f"Общий винрейт: {stats ['overall_win_rate']*100 :.1f}%")
        report .append (f"Уникальных карт: {stats ['unique_cards_used']}")
        if stats ['most_played_card']:
            report .append (f"\nСамая используемая: {stats ['most_played_card']}")
        if stats ['highest_winrate_card']:
            report .append (f"Лучший винрейт: {stats ['highest_winrate_card']}")
        report .append ("\nТОП-5 КОМБО:")
        for i ,combo in enumerate (self .get_best_combos (5 ),1 ):
            report .append (f"  {i }. {', '.join (combo ['cards'])} - {combo ['win_rate']*100 :.1f}%")
        return "\n".join (report )