from typing import List ,Dict ,Optional
class CounterPickTable :
    COUNTERS ={
    'golem':['inferno_tower','inferno_dragon','pekka','mini_pekka',
    'skeleton_army','minion_horde','cannon'],
    'giant':['inferno_tower','mini_pekka','pekka','skeleton_army',
    'cannon','tombstone'],
    'pekka':['inferno_tower','skeleton_army','minion_horde',
    'goblin_gang','swarm'],
    'mega_knight':['pekka','inferno_tower','knight','valkyrie',
    'mini_pekka'],
    'royal_giant':['inferno_tower','mini_pekka','pekka',
    'minion_horde','tesla'],
    'giant_skeleton':['inferno_tower','pekka','skeleton_army'],
    'lava_hound':['inferno_tower','inferno_dragon','minion_horde',
    'mega_minion','musketeer'],
    'electro_giant':['pekka','mini_pekka','skeleton_army',
    'minion_horde'],
    'hog_rider':['tornado','cannon','tesla','mini_pekka',
    'tombstone','skeleton_army','goblin_gang'],
    'balloon':['minion_horde','mega_minion','musketeer',
    'electro_wizard','inferno_dragon','tesla'],
    'ram_rider':['pekka','mini_pekka','cannon','tombstone'],
    'xbow':['earthquake','royal_giant','giant','golem','rocket'],
    'mortar':['knight','earthquake','royal_giant'],
    'goblin_barrel':['the_log','arrows','tornado','skeleton_army'],
    'graveyard':['poison','valkyrie','archers','skeleton_army'],
    'miner':['skeletons','goblin_gang','knight','valkyrie'],
    'sparky':['zap','electro_wizard','lightning','rocket',
    'skeleton_army'],
    'minion_horde':['arrows','fireball','wizard','baby_dragon',
    'poison','executioner'],
    'minions':['arrows','zap','mega_minion','musketeer'],
    'mega_minion':['musketeer','archers','electro_wizard'],
    'baby_dragon':['musketeer','mega_minion','inferno_dragon'],
    'inferno_dragon':['electro_wizard','zap','lightning','minions'],
    'electro_dragon':['lightning','rocket','mega_minion'],
    'bats':['zap','arrows','giant_snowball','electro_wizard'],
    'musketeer':['fireball','lightning','knight','mini_pekka'],
    'wizard':['fireball','lightning','rocket','mini_pekka'],
    'witch':['fireball','lightning','valkyrie','baby_dragon'],
    'electro_wizard':['fireball','lightning','mini_pekka','knight'],
    'night_witch':['poison','valkyrie','executioner'],
    'magic_archer':['fireball','lightning','mini_pekka'],
    'princess':['the_log','arrows','miner','goblin_barrel'],
    'hunter':['fireball','lightning','skeleton_army'],
    'knight':['skeleton_army','minion_horde','goblin_gang'],
    'valkyrie':['skeleton_army','minion_horde','pekka'],
    'mini_pekka':['skeleton_army','goblin_gang','guards'],
    'lumberjack':['skeleton_army','pekka','mini_pekka'],
    'dark_prince':['skeleton_army','pekka','minion_horde'],
    'prince':['skeleton_army','goblin_gang','guards','tombstone'],
    'bandit':['skeleton_army','goblin_gang','knight'],
    'skeleton_army':['the_log','arrows','zap','valkyrie',
    'baby_dragon','wizard'],
    'goblin_gang':['the_log','arrows','zap','valkyrie'],
    'guards':['valkyrie','baby_dragon','fireball'],
    'elixir_collector':['rocket','lightning','miner','fireball'],
    'inferno_tower':['zap','lightning','electro_wizard','minion_horde'],
    'tesla':['earthquake','lightning','rocket'],
    'bomb_tower':['lightning','rocket','miner'],
    'goblin_hut':['poison','fireball','miner','earthquake'],
    'furnace':['poison','fireball','miner'],
    }
    COUNTER_TYPES ={
    'hard':'Полностью нейтрализует с выгодой по эликсиру',
    'soft':'Эффективно защищает',
    'trade':'Защищает с равным обменом',
    'risky':'Защищает, но может быть обыграно'
    }
    def __init__ (self ):
        pass
    def get_counters (self ,card_name :str ,limit :int =5 )->List [str ]:
        card_name =card_name .lower ().replace (' ','_')
        counters =self .COUNTERS .get (card_name ,[])
        return counters [:limit ]
    def get_best_counter (self ,card_name :str )->Optional [str ]:
        counters =self .get_counters (card_name ,1 )
        return counters [0 ]if counters else None
    def find_counter_in_deck (self ,threat_card :str ,our_deck :List [str ])->List [str ]:
        counters =self .get_counters (threat_card )
        our_counters =[c for c in counters if c in our_deck ]
        return our_counters
    def is_countered_by (self ,card :str ,potential_counter :str )->bool :
        counters =self .get_counters (card )
        return potential_counter in counters
    def get_cards_countered_by (self ,counter_card :str )->List [str ]:
        result =[]
        for card ,counters in self .COUNTERS .items ():
            if counter_card in counters :
                result .append (card )
        return result
    def analyze_deck_weaknesses (self ,deck :List [str ])->Dict :
        weaknesses ={}
        threats =['golem','hog_rider','balloon','pekka','mega_knight',
        'xbow','goblin_barrel','lava_hound','graveyard']
        for threat in threats :
            counters_in_deck =self .find_counter_in_deck (threat ,deck )
            if not counters_in_deck :
                weaknesses [threat ]={
                'severity':'high',
                'message':f'Нет контры для {threat }',
                'suggestions':self .get_counters (threat ,3 )
                }
            elif len (counters_in_deck )==1 :
                weaknesses [threat ]={
                'severity':'medium',
                'message':f'Только 1 контра для {threat }',
                'our_counter':counters_in_deck [0 ]
                }
        return weaknesses
    def get_counter_priority (self ,threats :List [str ],our_hand :List [str ])->Dict :
        priorities =[]
        for threat in threats :
            for card in our_hand :
                if self .is_countered_by (threat ,card ):
                    priority =self .get_counters (threat ).index (card )if card in self .get_counters (threat )else 999
                    priorities .append ({
                    'threat':threat ,
                    'counter':card ,
                    'priority':priority
                    })
        priorities .sort (key =lambda x :x ['priority'])
        return priorities