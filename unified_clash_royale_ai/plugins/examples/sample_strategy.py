from ..plugin_base import StrategyPlugin
from typing import Dict ,Optional
class AggressiveStrategyPlugin (StrategyPlugin ):
    name ="Агрессивная стратегия"
    version ="1.0.0"
    author ="Столкновение Рояль ИИ"
    description ="Агрессивная стратегия - атакует при любой возможности"
    def __init__ (self ):
        super ().__init__ ()
        self .min_elixir_to_attack =4
    def on_load (self ):
        print (f"Загружен плагин: {self .name }")
    def on_unload (self ):
        print (f"Выгружен плагин: {self .name }")
    def get_priority (self )->int :
        return 50
    def should_activate (self ,game_state :Dict )->bool :
        elixir =game_state .get ('our_elixir',0 )
        return elixir >=self .min_elixir_to_attack
    def decide_action (self ,game_state :Dict )->Optional [Dict ]:
        elixir =game_state .get ('our_elixir',0 )
        hand =game_state .get ('our_hand',[])
        if not hand :
            return None
        win_conditions =['hog_rider','balloon','giant','golem','ram_rider']
        support =['musketeer','wizard','electro_wizard','mini_pekka']
        if elixir >=7 :
            for card in hand :
                if card .lower ()in win_conditions :
                    return {
                    'action':'play_card',
                    'card':card ,
                    'position':'bridge_left'
                    }
        if elixir >=4 :
            for card in hand :
                if card .lower ()in support :
                    return {
                    'action':'play_card',
                    'card':card ,
                    'position':'center_back'
                    }
        return None
    def on_action_executed (self ,action :Dict ,result :Dict ):
        print (f"[{self .name }] Выполнено действие: {action }")
class DefensiveStrategyPlugin (StrategyPlugin ):
    name ="Оборонительная стратегия"
    version ="1.0.0"
    author ="Столкновение Рояль ИИ"
    description ="Защитная стратегия - приоритет на защиту"
    def on_load (self ):
        print (f"Загружен плагин: {self .name }")
    def on_unload (self ):
        print (f"Выгружен плагин: {self .name }")
    def get_priority (self )->int :
        return 70
    def should_activate (self ,game_state :Dict )->bool :
        enemy_units =game_state .get ('enemy_units',[])
        return len (enemy_units )>0
    def decide_action (self ,game_state :Dict )->Optional [Dict ]:
        enemy_units =game_state .get ('enemy_units',[])
        hand =game_state .get ('our_hand',[])
        elixir =game_state .get ('our_elixir',0 )
        if not enemy_units or not hand :
            return None
        defensive_cards =['skeleton_army','mini_pekka','pekka',
        'cannon','tesla','inferno_tower']
        for card in hand :
            if card .lower ()in defensive_cards :
                card_cost =self ._get_card_cost (card )
                if elixir >=card_cost :
                    return {
                    'action':'play_card',
                    'card':card ,
                    'position':'center_mid'
                    }
        return None
    def _get_card_cost (self ,card :str )->int :
        costs ={
        'skeleton_army':3 ,
        'mini_pekka':4 ,
        'pekka':7 ,
        'cannon':3 ,
        'tesla':4 ,
        'inferno_tower':5
        }
        return costs .get (card .lower (),4 )