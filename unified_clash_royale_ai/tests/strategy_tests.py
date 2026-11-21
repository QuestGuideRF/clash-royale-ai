import random
from dataclasses import dataclass
from typing import List ,Dict ,Optional
@dataclass
class SimulatedCard :
    name :str
    elixir :int
    damage :int
    hp :int
    is_spell :bool =False
@dataclass
class SimulatedTower :
    hp :int
    max_hp :int =2534
class GameSimulator :
    def __init__ (self ):
        self .reset ()
        self .card_stats ={
        'knight':{'elixir':3 ,'damage':167 ,'hp':1399 ,'is_spell':False },
        'archers':{'elixir':3 ,'damage':107 ,'hp':304 ,'is_spell':False },
        'fireball':{'elixir':4 ,'damage':572 ,'hp':0 ,'is_spell':True },
        'zap':{'elixir':2 ,'damage':192 ,'hp':0 ,'is_spell':True },
        'hog_rider':{'elixir':4 ,'damage':264 ,'hp':1408 ,'is_spell':False },
        'musketeer':{'elixir':4 ,'damage':181 ,'hp':598 ,'is_spell':False },
        'giant':{'elixir':5 ,'damage':176 ,'hp':3275 ,'is_spell':False },
        'golem':{'elixir':8 ,'damage':259 ,'hp':4256 ,'is_spell':False },
        'skeleton_army':{'elixir':3 ,'damage':67 ,'hp':67 ,'is_spell':False },
        }
    def reset (self ):
        self .our_elixir =5.0
        self .opponent_elixir =5.0
        self .game_time =180
        self .our_towers =[
        SimulatedTower (hp =2534 ),
        SimulatedTower (hp =2534 ),
        SimulatedTower (hp =4008 ,max_hp =4008 )
        ]
        self .opponent_towers =[
        SimulatedTower (hp =2534 ),
        SimulatedTower (hp =2534 ),
        SimulatedTower (hp =4008 ,max_hp =4008 )
        ]
        self .our_units =[]
        self .opponent_units =[]
        self .turn =0
    def simulate_turn (self ,our_action =None ,opponent_action =None ):
        regen_rate =2.8 if self .game_time >60 else 1.4
        elixir_gain =1.0 /regen_rate
        self .our_elixir =min (10 ,self .our_elixir +elixir_gain )
        self .opponent_elixir =min (10 ,self .opponent_elixir +elixir_gain )
        if our_action and our_action in self .card_stats :
            card =self .card_stats [our_action ]
            if self .our_elixir >=card ['elixir']:
                self .our_elixir -=card ['elixir']
                if card ['is_spell']:
                    self ._apply_spell_damage (card ['damage'],target ='opponent')
                else :
                    self .our_units .append ({
                    'name':our_action ,
                    'hp':card ['hp'],
                    'damage':card ['damage']
                    })
        if opponent_action and opponent_action in self .card_stats :
            card =self .card_stats [opponent_action ]
            if self .opponent_elixir >=card ['elixir']:
                self .opponent_elixir -=card ['elixir']
                if card ['is_spell']:
                    self ._apply_spell_damage (card ['damage'],target ='our')
                else :
                    self .opponent_units .append ({
                    'name':opponent_action ,
                    'hp':card ['hp'],
                    'damage':card ['damage']
                    })
        self ._simulate_combat ()
        self .game_time -=1
        self .turn +=1
    def _apply_spell_damage (self ,damage ,target ):
        if target =='opponent':
            tower_damage =int (damage *0.35 )
            for tower in self .opponent_towers :
                if tower .hp >0 :
                    tower .hp -=tower_damage
                    break
        else :
            tower_damage =int (damage *0.35 )
            for tower in self .our_towers :
                if tower .hp >0 :
                    tower .hp -=tower_damage
                    break
    def _simulate_combat (self ):
        for unit in self .our_units [:]:
            for tower in self .opponent_towers :
                if tower .hp >0 :
                    tower .hp -=unit ['damage']
                    break
            unit ['hp']-=100
            if unit ['hp']<=0 :
                self .our_units .remove (unit )
        for unit in self .opponent_units [:]:
            for tower in self .our_towers :
                if tower .hp >0 :
                    tower .hp -=unit ['damage']
                    break
            unit ['hp']-=100
            if unit ['hp']<=0 :
                self .opponent_units .remove (unit )
    def get_our_crowns (self ):
        crowns =sum (1 for t in self .opponent_towers if t .hp <=0 )
        return min (3 ,crowns )
    def get_opponent_crowns (self ):
        crowns =sum (1 for t in self .our_towers if t .hp <=0 )
        return min (3 ,crowns )
    def is_game_over (self ):
        if self .game_time <=0 :
            return True
        if self .get_our_crowns ()>=3 or self .get_opponent_crowns ()>=3 :
            return True
        return False
    def get_result (self ):
        our_crowns =self .get_our_crowns ()
        opp_crowns =self .get_opponent_crowns ()
        if our_crowns >opp_crowns :
            return 'win'
        elif opp_crowns >our_crowns :
            return 'loss'
        else :
            return 'draw'
class StrategyTester :
    def __init__ (self ):
        self .simulator =GameSimulator ()
        self .results =[]
    def test_strategy (self ,strategy_func ,opponent_strategy =None ,
    num_games =100 ,deck =None ):
        if deck is None :
            deck =['knight','archers','fireball','zap',
            'hog_rider','musketeer','giant','skeleton_army']
        wins =0
        losses =0
        draws =0
        for _ in range (num_games ):
            self .simulator .reset ()
            while not self .simulator .is_game_over ():
                state ={
                'our_elixir':self .simulator .our_elixir ,
                'opponent_elixir':self .simulator .opponent_elixir ,
                'game_time':self .simulator .game_time ,
                'our_towers':self .simulator .our_towers ,
                'opponent_towers':self .simulator .opponent_towers ,
                'deck':deck
                }
                our_action =strategy_func (state )
                if opponent_strategy :
                    opp_action =opponent_strategy (state )
                else :
                    opp_action =self ._random_opponent_action ()
                self .simulator .simulate_turn (our_action ,opp_action )
            result =self .simulator .get_result ()
            if result =='win':
                wins +=1
            elif result =='loss':
                losses +=1
            else :
                draws +=1
        win_rate =wins /num_games
        self .results .append ({
        'strategy':strategy_func .__name__ if hasattr (strategy_func ,'__name__')else 'custom',
        'games':num_games ,
        'wins':wins ,
        'losses':losses ,
        'draws':draws ,
        'win_rate':win_rate
        })
        return {
        'wins':wins ,
        'losses':losses ,
        'draws':draws ,
        'win_rate':win_rate
        }
    def _random_opponent_action (self ):
        cards =['knight','archers','fireball','hog_rider']
        if random .random ()>0.5 :
            return random .choice (cards )
        return None
    def compare_strategies (self ,strategies ,num_games =100 ):
        results =[]
        for strategy in strategies :
            result =self .test_strategy (strategy ,num_games =num_games )
            result ['name']=strategy .__name__ if hasattr (strategy ,'__name__')else str (strategy )
            results .append (result )
        results .sort (key =lambda x :x ['win_rate'],reverse =True )
        return results
def aggressive_strategy (state ):
    if state ['our_elixir']>=4 :
        return 'hog_rider'
    elif state ['our_elixir']>=3 :
        return 'knight'
    return None
def defensive_strategy (state ):
    if state ['our_elixir']>=10 :
        return 'giant'
    elif state ['our_elixir']>=3 :
        return 'archers'
    return None
def cycle_strategy (state ):
    if state ['our_elixir']>=8 :
        return 'hog_rider'
    elif state ['our_elixir']>=6 :
        return 'musketeer'
    return None
def elixir_advantage_strategy (state ):
    advantage =state ['our_elixir']-state ['opponent_elixir']
    if advantage >=3 and state ['our_elixir']>=4 :
        return 'hog_rider'
    elif state ['our_elixir']>=10 :
        return 'giant'
    return None