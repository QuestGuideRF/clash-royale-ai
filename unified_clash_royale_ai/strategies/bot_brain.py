import random
import numpy as np
from ..data .cards_database import CARDS_DATABASE ,get_card_info ,get_counter_cards
class BotBrain :
    def __init__ (self ,game_state ,action_executor ,troop_detector =None ):
        self .game_state =game_state
        self .action_executor =action_executor
        self .troop_detector =troop_detector
        self .current_strategy ='balanced'
        self .elixir_advantage_threshold =2
        self .positions ={
        'bridge_left':(128 ,438 ),
        'bridge_right':(419 ,457 ),
        'defense_center':(265 ,560 ),
        'king_tower_front':(274 ,650 ),
        'back_left':(47 ,750 ),
        'back_right':(502 ,751 ),
        'anti_air_left':(150 ,550 ),
        'anti_air_right':(400 ,550 ),
        'building_optimal':(265 ,480 )
        }
        self .card_priorities ={
        'win_condition':10 ,
        'tank_killer':9 ,
        'area_damage':8 ,
        'support':7 ,
        'building':6 ,
        'swarm':5 ,
        'cycle':4 ,
        'spell':3
        }
    def analyze_situation (self ,enemy_troops ,ally_troops ):
        analysis ={
        'threat_level':0 ,
        'attack_opportunity':0 ,
        'elixir_advantage':0 ,
        'enemy_push_side':None ,
        'priority_target':None ,
        'recommended_action':None
        }
        enemy_count =len (enemy_troops .get ('all',([],[]))[0 ])
        attacking_enemies =self ._get_attacking_troops (enemy_troops )
        if attacking_enemies :
            analysis ['threat_level']=min (10 ,len (attacking_enemies )*2 )
            analysis ['enemy_push_side']=self ._determine_push_side (attacking_enemies )
            analysis ['priority_target']=self ._find_priority_target (attacking_enemies )
        ally_count =len (ally_troops .get ('all',([],[]))[0 ])
        if ally_count >enemy_count and self .game_state .elixir_blue >=5 :
            analysis ['attack_opportunity']=min (10 ,(ally_count -enemy_count )*2 )
        analysis ['elixir_advantage']=self .game_state .elixir_blue -5
        if analysis ['threat_level']>=7 :
            analysis ['recommended_action']='defend'
        elif analysis ['attack_opportunity']>=6 and analysis ['elixir_advantage']>=2 :
            analysis ['recommended_action']='attack'
        elif analysis ['threat_level']>=4 :
            analysis ['recommended_action']='counter_push'
        else :
            analysis ['recommended_action']='wait'
        return analysis
    def _get_attacking_troops (self ,enemy_troops ):
        attacking =[]
        all_troops =enemy_troops .get ('all',([],[]))
        for i ,troop in enumerate (all_troops [0 ]):
            if len (all_troops [1 ])>i :
                pos =all_troops [1 ][i ]
                if pos [1 ]>400 :
                    attacking .append ((troop ,pos ))
        return attacking
    def _determine_push_side (self ,attacking_troops ):
        left_count =0
        right_count =0
        for troop ,pos in attacking_troops :
            if pos [0 ]<265 :
                left_count +=1
            else :
                right_count +=1
        if left_count >right_count :
            return 'left'
        elif right_count >left_count :
            return 'right'
        return 'center'
    def _find_priority_target (self ,attacking_troops ):
        highest_priority =None
        highest_score =0
        for troop ,pos in attacking_troops :
            troop_name =troop .replace ('enemy_','')
            card_info =get_card_info (troop_name )
            if card_info :
                score =0
                tags =card_info .get ('tags',[])
                if 'win_condition'in tags :
                    score +=10
                if 'tank'in tags :
                    score +=8
                if card_info .get ('elixir',0 )>=5 :
                    score +=5
                distance_to_tower =abs (650 -pos [1 ])
                score +=(300 -distance_to_tower )/30
                if score >highest_score :
                    highest_score =score
                    highest_priority =(troop ,pos )
        return highest_priority
    def decide_action (self ,enemy_troops ,ally_troops ):
        analysis =self .analyze_situation (enemy_troops ,ally_troops )
        cards_in_hand =list (self .game_state .cards_in_hand .values ())
        available_cards =[(i ,card )for i ,card in enumerate (cards_in_hand )if card ]
        if not available_cards :
            return None
        action =analysis ['recommended_action']
        if action =='defend':
            return self ._decide_defense (analysis ,available_cards )
        elif action =='attack':
            return self ._decide_attack (analysis ,available_cards )
        elif action =='counter_push':
            return self ._decide_counter_push (analysis ,available_cards )
        else :
            return self ._decide_wait (analysis ,available_cards )
    def _decide_defense (self ,analysis ,available_cards ):
        priority_target =analysis .get ('priority_target')
        push_side =analysis .get ('enemy_push_side','center')
        best_card =None
        best_score =0
        for i ,card in available_cards :
            card_name =card .replace ('ally_','')
            card_info =get_card_info (card_name )
            if not card_info :
                continue
            cost =card_info .get ('elixir',10 )
            if cost >self .game_state .elixir_blue :
                continue
            score =0
            tags =card_info .get ('tags',[])
            if 'tank_killer'in tags :
                score +=10
            if 'area_damage'in tags :
                score +=8
            if 'defensive'in tags :
                score +=7
            if 'swarm'in tags and priority_target :
                target_name =priority_target [0 ].replace ('enemy_','')
                target_info =get_card_info (target_name )
                if target_info and not target_info .get ('area_damage',False ):
                    score +=6
            score -=cost *0.5
            if score >best_score :
                best_score =score
                best_card =(i ,card )
        if best_card :
            if priority_target :
                target_pos =priority_target [1 ]
                defense_pos =(target_pos [0 ],min (target_pos [1 ]+50 ,700 ))
            else :
                defense_pos =self .positions ['defense_center']
            return (best_card [0 ],defense_pos )
        return None
    def _decide_attack (self ,analysis ,available_cards ):
        target_tower ='left'if self .game_state .tower_hp_red [0 ]<=self .game_state .tower_hp_red [1 ]else 'right'
        win_con =None
        support =None
        for i ,card in available_cards :
            card_name =card .replace ('ally_','')
            card_info =get_card_info (card_name )
            if not card_info :
                continue
            tags =card_info .get ('tags',[])
            cost =card_info .get ('elixir',10 )
            if cost >self .game_state .elixir_blue :
                continue
            if 'win_condition'in tags and not win_con :
                win_con =(i ,card ,card_info )
            elif 'support'in tags and not support :
                support =(i ,card ,card_info )
        if win_con :
            bridge_pos =self .positions [f'bridge_{target_tower }']
            return (win_con [0 ],bridge_pos )
        return None
    def _decide_counter_push (self ,analysis ,available_cards ):
        for i ,card in available_cards :
            card_name =card .replace ('ally_','')
            card_info =get_card_info (card_name )
            if not card_info :
                continue
            tags =card_info .get ('tags',[])
            cost =card_info .get ('elixir',10 )
            if cost >self .game_state .elixir_blue :
                continue
            if 'support'in tags and cost <=4 :
                push_side =analysis .get ('enemy_push_side','left')
                pos =self .positions [f'bridge_{push_side }']
                return (i ,pos )
        return None
    def _decide_wait (self ,analysis ,available_cards ):
        if self .game_state .elixir_blue >=9 :
            for i ,card in available_cards :
                card_name =card .replace ('ally_','')
                card_info =get_card_info (card_name )
                if not card_info :
                    continue
                cost =card_info .get ('elixir',10 )
                if cost <=3 :
                    return (i ,self .positions ['back_left'])
        return None
    def execute_action (self ,action ):
        if action is None :
            return False
        card_index ,position =action
        card =self .game_state .cards_in_hand .get (card_index )
        if not card :
            return False
        card_name =card .replace ('ally_','')
        card_info =get_card_info (card_name )
        if card_info :
            cost =card_info .get ('elixir',0 )
            if cost >self .game_state .elixir_blue :
                return False
        self .action_executor .place_card (card_index ,position )
        return True