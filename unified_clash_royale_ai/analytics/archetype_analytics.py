import json
import os
from typing import Dict ,List ,Optional
from collections import defaultdict
class ArchetypeAnalytics :
    ARCHETYPES ={
    'beatdown':['golem','giant','lava_hound','elixir_collector'],
    'cycle':['hog_rider','ice_spirit','skeletons','ice_golem'],
    'control':['pekka','poison','tornado','mega_knight'],
    'siege':['xbow','mortar','tesla'],
    'bait':['goblin_barrel','princess','goblin_gang','inferno_tower'],
    'bridge_spam':['battle_ram','bandit','royal_ghost','ram_rider'],
    'graveyard':['graveyard','poison','baby_dragon','tornado'],
    'three_musketeers':['three_musketeers','elixir_collector','minion_horde']
    }
    def __init__ (self ,data_file :str ="data/archetype_analytics.json"):
        self .data_file =data_file
        self .data =self ._load_data ()
    def _load_data (self )->Dict :
        if os .path .exists (self .data_file ):
            with open (self .data_file ,'r',encoding ='utf-8')as f :
                return json .load (f )
        return {
        'archetypes':{},
        'matchups':{},
        'trends':[]
        }
    def _save_data (self ):
        os .makedirs (os .path .dirname (self .data_file )or '.',exist_ok =True )
        with open (self .data_file ,'w',encoding ='utf-8')as f :
            json .dump (self .data ,f ,indent =2 ,ensure_ascii =False )
    def detect_archetype (self ,deck :List [str ])->str :
        deck_set =set (c .lower ().replace (' ','_')for c in deck )
        best_match =None
        best_score =0
        for archetype ,markers in self .ARCHETYPES .items ():
            score =len (set (markers )&deck_set )
            if score >best_score :
                best_score =score
                best_match =archetype
        return best_match if best_score >=2 else 'unknown'
    def record_match (self ,our_deck :List [str ],opponent_deck :List [str ],
    result :str ,crowns_us :int =0 ,crowns_them :int =0 ):
        our_archetype =self .detect_archetype (our_deck )
        opponent_archetype =self .detect_archetype (opponent_deck )
        if our_archetype not in self .data ['archetypes']:
            self .data ['archetypes'][our_archetype ]={
            'games':0 ,
            'wins':0 ,
            'losses':0 ,
            'draws':0 ,
            'crowns_for':0 ,
            'crowns_against':0
            }
        arch_data =self .data ['archetypes'][our_archetype ]
        arch_data ['games']+=1
        arch_data ['crowns_for']+=crowns_us
        arch_data ['crowns_against']+=crowns_them
        if result =='win':
            arch_data ['wins']+=1
        elif result =='loss':
            arch_data ['losses']+=1
        else :
            arch_data ['draws']+=1
        matchup_key =f"{our_archetype }_vs_{opponent_archetype }"
        if matchup_key not in self .data ['matchups']:
            self .data ['matchups'][matchup_key ]={
            'our_archetype':our_archetype ,
            'opponent_archetype':opponent_archetype ,
            'games':0 ,
            'wins':0 ,
            'losses':0
            }
        self .data ['matchups'][matchup_key ]['games']+=1
        if result =='win':
            self .data ['matchups'][matchup_key ]['wins']+=1
        elif result =='loss':
            self .data ['matchups'][matchup_key ]['losses']+=1
        self ._save_data ()
    def get_archetype_stats (self ,archetype :str )->Optional [Dict ]:
        if archetype not in self .data ['archetypes']:
            return None
        data =self .data ['archetypes'][archetype ]
        total =data ['wins']+data ['losses']+data ['draws']
        return {
        'archetype':archetype ,
        'games':data ['games'],
        'win_rate':data ['wins']/total if total >0 else 0 ,
        'avg_crowns_for':(
        data ['crowns_for']/data ['games']
        if data ['games']>0 else 0
        ),
        'avg_crowns_against':(
        data ['crowns_against']/data ['games']
        if data ['games']>0 else 0
        )
        }
    def get_matchup_stats (self ,our_archetype :str ,
    opponent_archetype :str )->Optional [Dict ]:
        matchup_key =f"{our_archetype }_vs_{opponent_archetype }"
        if matchup_key not in self .data ['matchups']:
            return None
        data =self .data ['matchups'][matchup_key ]
        total =data ['wins']+data ['losses']
        return {
        'our_archetype':our_archetype ,
        'opponent_archetype':opponent_archetype ,
        'games':data ['games'],
        'win_rate':data ['wins']/total if total >0 else 0.5
        }
    def get_best_archetype (self )->Optional [Dict ]:
        best =None
        best_wr =0
        for archetype ,data in self .data ['archetypes'].items ():
            total =data ['wins']+data ['losses']
            if total >=10 :
                wr =data ['wins']/total
                if wr >best_wr :
                    best_wr =wr
                    best =archetype
        return self .get_archetype_stats (best )if best else None
    def get_worst_matchups (self ,our_archetype :str ,limit :int =5 )->List [Dict ]:
        matchups =[]
        for key ,data in self .data ['matchups'].items ():
            if data ['our_archetype']==our_archetype :
                total =data ['wins']+data ['losses']
                if total >=5 :
                    matchups .append ({
                    'opponent':data ['opponent_archetype'],
                    'games':data ['games'],
                    'win_rate':data ['wins']/total
                    })
        matchups .sort (key =lambda x :x ['win_rate'])
        return matchups [:limit ]
    def get_best_matchups (self ,our_archetype :str ,limit :int =5 )->List [Dict ]:
        matchups =[]
        for key ,data in self .data ['matchups'].items ():
            if data ['our_archetype']==our_archetype :
                total =data ['wins']+data ['losses']
                if total >=5 :
                    matchups .append ({
                    'opponent':data ['opponent_archetype'],
                    'games':data ['games'],
                    'win_rate':data ['wins']/total
                    })
        matchups .sort (key =lambda x :x ['win_rate'],reverse =True )
        return matchups [:limit ]
    def get_matchup_table (self )->Dict [str ,Dict [str ,float ]]:
        table ={}
        archetypes =list (self .ARCHETYPES .keys ())+['unknown']
        for our in archetypes :
            table [our ]={}
            for opp in archetypes :
                stats =self .get_matchup_stats (our ,opp )
                table [our ][opp ]=stats ['win_rate']if stats else 0.5
        return table
    def generate_report (self )->str :
        report =[]
        report .append ("="*60 )
        report .append ("АНАЛИТИКА АРХЕТИПОВ")
        report .append ("="*60 )
        report .append ("\nСТАТИСТИКА ПО АРХЕТИПАМ:")
        for archetype in self .ARCHETYPES .keys ():
            stats =self .get_archetype_stats (archetype )
            if stats and stats ['games']>0 :
                report .append (
                f"  {archetype }: {stats ['games']} игр, "
                f"{stats ['win_rate']*100 :.1f}% WR"
                )
        best =self .get_best_archetype ()
        if best :
            report .append (f"\nЛучший архетип: {best ['archetype']} ({best ['win_rate']*100 :.1f}%)")
        return "\n".join (report )