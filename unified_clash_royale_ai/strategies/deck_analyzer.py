from ..data .cards_database import CARDS_DATABASE ,get_card_info
class DeckAnalyzer :
    def __init__ (self ):
        self .known_archetypes ={
        'beatdown':['golem','giant','lava_hound','elixir_golem'],
        'control':['x_bow','mortar','rocket','tesla'],
        'bridge_spam':['bandit','battle_ram','ram_rider','royal_ghost'],
        'cycle':['hog_rider','miner','balloon','wall_breakers'],
        'bait':['goblin_barrel','princess','goblin_gang','skeleton_army']
        }
    def analyze_deck (self ,deck_cards ):
        analysis ={
        'archetype':None ,
        'avg_elixir':0 ,
        'win_conditions':[],
        'spells':[],
        'anti_air':[],
        'tank_killers':[],
        'weaknesses':[],
        'strengths':[]
        }
        total_elixir =0
        card_count =0
        for card in deck_cards :
            if not card or card =='MysteryCard':
                continue
            card_name =card .lower ().replace ('ally_','').replace ('enemy_','')
            card_info =get_card_info (card_name )
            if not card_info :
                continue
            card_count +=1
            total_elixir +=card_info .get ('elixir',0 )
            tags =card_info .get ('tags',[])
            if 'win_condition'in tags :
                analysis ['win_conditions'].append (card_name )
            if card_info .get ('type')=='spell':
                analysis ['spells'].append (card_name )
            if card_info .get ('targets')in ['air_ground','air']:
                analysis ['anti_air'].append (card_name )
            if 'tank_killer'in tags :
                analysis ['tank_killers'].append (card_name )
        if card_count >0 :
            analysis ['avg_elixir']=total_elixir /card_count
        analysis ['archetype']=self ._determine_archetype (deck_cards )
        analysis ['weaknesses']=self ._find_weaknesses (analysis )
        analysis ['strengths']=self ._find_strengths (analysis )
        return analysis
    def _determine_archetype (self ,deck_cards ):
        deck_lower =[c .lower ().replace ('ally_','').replace ('enemy_','')
        for c in deck_cards if c and c !='MysteryCard']
        best_match =None
        best_score =0
        for archetype ,key_cards in self .known_archetypes .items ():
            score =sum (1 for card in key_cards if card in deck_lower )
            if score >best_score :
                best_score =score
                best_match =archetype
        return best_match if best_score >0 else 'unknown'
    def _find_weaknesses (self ,analysis ):
        weaknesses =[]
        if not analysis ['anti_air']:
            weaknesses .append ('vulnerable_to_air')
        if not analysis ['tank_killers']:
            weaknesses .append ('vulnerable_to_tanks')
        if analysis ['avg_elixir']>4.0 :
            weaknesses .append ('high_cost_deck')
        if not analysis ['spells']:
            weaknesses .append ('no_spells')
        return weaknesses
    def _find_strengths (self ,analysis ):
        strengths =[]
        if len (analysis ['win_conditions'])>=2 :
            strengths .append ('multiple_win_conditions')
        if analysis ['avg_elixir']<3.5 :
            strengths .append ('cycle_potential')
        if len (analysis ['anti_air'])>=3 :
            strengths .append ('strong_anti_air')
        if len (analysis ['tank_killers'])>=2 :
            strengths .append ('strong_tank_counters')
        return strengths
    def suggest_counters (self ,opponent_deck ):
        analysis =self .analyze_deck (opponent_deck )
        suggestions =[]
        archetype =analysis .get ('archetype')
        if archetype =='beatdown':
            suggestions .extend (['inferno_tower','mini_pekka','pekka','inferno_dragon'])
        elif archetype =='cycle':
            suggestions .extend (['cannon','tesla','tornado','bomb_tower'])
        elif archetype =='bait':
            suggestions .extend (['arrows','log','zap','valkyrie'])
        elif archetype =='bridge_spam':
            suggestions .extend (['mega_knight','valkyrie','bomb_tower','tornado'])
        for win_con in analysis .get ('win_conditions',[]):
            counters =self ._get_specific_counter (win_con )
            suggestions .extend (counters )
        return list (set (suggestions ))[:8 ]
    def _get_specific_counter (self ,card_name ):
        counters_map ={
        'hog_rider':['cannon','tornado','mini_pekka','goblin_cage'],
        'balloon':['musketeer','wizard','minions','electro_wizard'],
        'golem':['inferno_tower','pekka','mini_pekka','inferno_dragon'],
        'giant':['inferno_tower','mini_pekka','pekka'],
        'x_bow':['earthquake','rocket','giant'],
        'graveyard':['poison','valkyrie','archers'],
        'goblin_barrel':['log','arrows','barbarian_barrel'],
        'lava_hound':['minions','mega_minion','inferno_tower']
        }
        return counters_map .get (card_name ,[])