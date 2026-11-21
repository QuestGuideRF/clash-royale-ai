import os
import json
from datetime import datetime
from collections import defaultdict
class Statistics :
    def __init__ (self ,stats_file ="stats.json"):
        self .stats_file =stats_file
        self .stats =self ._load_stats ()
    def _load_stats (self ):
        if os .path .exists (self .stats_file ):
            try :
                with open (self .stats_file ,'r')as f :
                    return json .load (f )
            except :
                pass
        return {
        'total_matches':0 ,
        'wins':0 ,
        'losses':0 ,
        'draws':0 ,
        'total_crowns_won':0 ,
        'total_crowns_lost':0 ,
        'cards_played':defaultdict (int ),
        'win_conditions_used':defaultdict (int ),
        'successful_defenses':0 ,
        'failed_defenses':0 ,
        'average_elixir_advantage':0 ,
        'matches_history':[]
        }
    def _save_stats (self ):
        stats_to_save =self .stats .copy ()
        stats_to_save ['cards_played']=dict (self .stats ['cards_played'])
        stats_to_save ['win_conditions_used']=dict (self .stats ['win_conditions_used'])
        with open (self .stats_file ,'w')as f :
            json .dump (stats_to_save ,f ,indent =2 )
    def record_match (self ,result ,crowns_won ,crowns_lost ,details =None ):
        self .stats ['total_matches']+=1
        if result =='win':
            self .stats ['wins']+=1
        elif result =='loss':
            self .stats ['losses']+=1
        else :
            self .stats ['draws']+=1
        self .stats ['total_crowns_won']+=crowns_won
        self .stats ['total_crowns_lost']+=crowns_lost
        match_record ={
        'date':datetime .now ().isoformat (),
        'result':result ,
        'crowns_won':crowns_won ,
        'crowns_lost':crowns_lost ,
        'details':details
        }
        self .stats ['matches_history'].append (match_record )
        if len (self .stats ['matches_history'])>100 :
            self .stats ['matches_history']=self .stats ['matches_history'][-100 :]
        self ._save_stats ()
    def record_card_played (self ,card_name ):
        self .stats ['cards_played'][card_name ]=self .stats ['cards_played'].get (card_name ,0 )+1
    def record_defense (self ,successful ):
        if successful :
            self .stats ['successful_defenses']+=1
        else :
            self .stats ['failed_defenses']+=1
    def get_win_rate (self ):
        total =self .stats ['wins']+self .stats ['losses']
        if total ==0 :
            return 0
        return self .stats ['wins']/total *100
    def get_most_played_cards (self ,top_n =10 ):
        cards =self .stats ['cards_played']
        sorted_cards =sorted (cards .items (),key =lambda x :x [1 ],reverse =True )
        return sorted_cards [:top_n ]
    def get_summary (self ):
        return {
        'total_matches':self .stats ['total_matches'],
        'wins':self .stats ['wins'],
        'losses':self .stats ['losses'],
        'draws':self .stats ['draws'],
        'win_rate':f"{self .get_win_rate ():.1f}%",
        'crown_difference':self .stats ['total_crowns_won']-self .stats ['total_crowns_lost'],
        'defense_success_rate':self ._get_defense_rate (),
        'most_played_cards':self .get_most_played_cards (5 )
        }
    def _get_defense_rate (self ):
        total =self .stats ['successful_defenses']+self .stats ['failed_defenses']
        if total ==0 :
            return "N/A"
        return f"{self .stats ['successful_defenses']/total *100 :.1f}%"
    def print_summary (self ):
        summary =self .get_summary ()
        print ("\n"+"="*50 )
        print ("📊 СТАТИСТИКА AI")
        print ("="*50 )
        print (f"Всего матчей: {summary ['total_matches']}")
        print (f"Победы: {summary ['wins']} | Поражения: {summary ['losses']} | Ничьи: {summary ['draws']}")
        print (f"Винрейт: {summary ['win_rate']}")
        print (f"Разница корон: {summary ['crown_difference']:+d}")
        print (f"Успешность защит: {summary ['defense_success_rate']}")
        print ("\nТоп-5 карт:")
        for card ,count in summary ['most_played_cards']:
            print (f"  {card }: {count } раз")
        print ("="*50 +"\n")