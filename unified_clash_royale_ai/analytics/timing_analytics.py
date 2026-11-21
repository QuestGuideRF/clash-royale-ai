import json
import os
from typing import Dict ,List ,Optional
from collections import defaultdict
class TimingAnalytics :
    def __init__ (self ,data_file :str ="data/timing_analytics.json"):
        self .data_file =data_file
        self .data =self ._load_data ()
    def _load_data (self )->Dict :
        if os .path .exists (self .data_file ):
            with open (self .data_file ,'r',encoding ='utf-8')as f :
                return json .load (f )
        return {
        'attacks':[],
        'by_time':defaultdict (lambda :{'total':0 ,'successful':0 }),
        'by_elixir':defaultdict (lambda :{'total':0 ,'successful':0 }),
        'by_phase':defaultdict (lambda :{'total':0 ,'successful':0 })
        }
    def _save_data (self ):
        os .makedirs (os .path .dirname (self .data_file )or '.',exist_ok =True )
        save_data ={
        'attacks':self .data ['attacks'],
        'by_time':dict (self .data ['by_time']),
        'by_elixir':dict (self .data ['by_elixir']),
        'by_phase':dict (self .data ['by_phase'])
        }
        with open (self .data_file ,'w',encoding ='utf-8')as f :
            json .dump (save_data ,f ,indent =2 ,ensure_ascii =False )
    def record_attack (self ,game_time :int ,elixir_spent :int ,
    our_elixir_before :int ,opponent_elixir_estimate :int ,
    cards_used :List [str ],damage_dealt :int ,
    tower_taken :bool =False ):
        attack ={
        'game_time':game_time ,
        'elixir_spent':elixir_spent ,
        'our_elixir':our_elixir_before ,
        'opponent_elixir':opponent_elixir_estimate ,
        'cards':cards_used ,
        'damage':damage_dealt ,
        'tower_taken':tower_taken ,
        'successful':damage_dealt >500 or tower_taken
        }
        self .data ['attacks'].append (attack )
        time_bucket =str ((game_time //30 )*30 )
        if time_bucket not in self .data ['by_time']:
            self .data ['by_time'][time_bucket ]={'total':0 ,'successful':0 }
        self .data ['by_time'][time_bucket ]['total']+=1
        if attack ['successful']:
            self .data ['by_time'][time_bucket ]['successful']+=1
        elixir_bucket =str (our_elixir_before )
        if elixir_bucket not in self .data ['by_elixir']:
            self .data ['by_elixir'][elixir_bucket ]={'total':0 ,'successful':0 }
        self .data ['by_elixir'][elixir_bucket ]['total']+=1
        if attack ['successful']:
            self .data ['by_elixir'][elixir_bucket ]['successful']+=1
        if game_time >120 :
            phase ='single'
        elif game_time >60 :
            phase ='double'
        else :
            phase ='triple'
        if phase not in self .data ['by_phase']:
            self .data ['by_phase'][phase ]={'total':0 ,'successful':0 }
        self .data ['by_phase'][phase ]['total']+=1
        if attack ['successful']:
            self .data ['by_phase'][phase ]['successful']+=1
        self ._save_data ()
    def get_best_attack_time (self )->Dict :
        best_time =None
        best_success_rate =0
        for time_bucket ,data in self .data ['by_time'].items ():
            if data ['total']>=10 :
                rate =data ['successful']/data ['total']
                if rate >best_success_rate :
                    best_success_rate =rate
                    best_time =int (time_bucket )
        if best_time is not None :
            return {
            'time_remaining':best_time ,
            'time_formatted':f"{best_time //60 }:{best_time %60 :02d}",
            'success_rate':best_success_rate
            }
        return None
    def get_best_elixir_to_attack (self )->Dict :
        best_elixir =None
        best_success_rate =0
        for elixir ,data in self .data ['by_elixir'].items ():
            if data ['total']>=10 :
                rate =data ['successful']/data ['total']
                if rate >best_success_rate :
                    best_success_rate =rate
                    best_elixir =int (elixir )
        if best_elixir is not None :
            return {
            'elixir':best_elixir ,
            'success_rate':best_success_rate
            }
        return None
    def get_phase_stats (self )->Dict :
        stats ={}
        for phase ,data in self .data ['by_phase'].items ():
            if data ['total']>0 :
                stats [phase ]={
                'attacks':data ['total'],
                'success_rate':data ['successful']/data ['total']
                }
        return stats
    def should_attack_now (self ,game_time :int ,our_elixir :int ,
    opponent_elixir_estimate :int )->Dict :
        time_bucket =str ((game_time //30 )*30 )
        elixir_bucket =str (our_elixir )
        time_stats =self .data ['by_time'].get (time_bucket ,{'total':0 ,'successful':0 })
        elixir_stats =self .data ['by_elixir'].get (elixir_bucket ,{'total':0 ,'successful':0 })
        time_rate =(
        time_stats ['successful']/time_stats ['total']
        if time_stats ['total']>0 else 0.5
        )
        elixir_rate =(
        elixir_stats ['successful']/elixir_stats ['total']
        if elixir_stats ['total']>0 else 0.5
        )
        elixir_advantage =our_elixir -opponent_elixir_estimate
        advantage_bonus =0.1 *max (-2 ,min (2 ,elixir_advantage ))
        combined_rate =(time_rate +elixir_rate )/2 +advantage_bonus
        recommendation ={
        'should_attack':combined_rate >=0.5 ,
        'confidence':combined_rate ,
        'factors':{
        'time_success_rate':time_rate ,
        'elixir_success_rate':elixir_rate ,
        'elixir_advantage':elixir_advantage
        }
        }
        if combined_rate >=0.7 :
            recommendation ['message']="Отличное время для атаки!"
        elif combined_rate >=0.5 :
            recommendation ['message']="Можно атаковать"
        elif combined_rate >=0.3 :
            recommendation ['message']="Рискованно, лучше подождать"
        else :
            recommendation ['message']="Не рекомендуется атаковать"
        return recommendation
    def generate_report (self )->str :
        report =[]
        report .append ("="*60 )
        report .append ("АНАЛИТИКА ТАЙМИНГА")
        report .append ("="*60 )
        total_attacks =len (self .data ['attacks'])
        successful =sum (1 for a in self .data ['attacks']if a .get ('successful'))
        report .append (f"\nВсего атак: {total_attacks }")
        report .append (f"Успешных: {successful } ({successful /total_attacks *100 :.1f}%)"
        if total_attacks >0 else "")
        best_time =self .get_best_attack_time ()
        if best_time :
            report .append (f"\nЛучшее время для атаки: {best_time ['time_formatted']}")
            report .append (f"  Успешность: {best_time ['success_rate']*100 :.1f}%")
        best_elixir =self .get_best_elixir_to_attack ()
        if best_elixir :
            report .append (f"\nОптимальный эликсир: {best_elixir ['elixir']}")
            report .append (f"  Успешность: {best_elixir ['success_rate']*100 :.1f}%")
        phase_stats =self .get_phase_stats ()
        report .append ("\nПО ФАЗАМ ИГРЫ:")
        for phase ,stats in phase_stats .items ():
            report .append (f"  {phase }: {stats ['attacks']} атак, "
            f"{stats ['success_rate']*100 :.1f}% успех")
        return "\n".join (report )