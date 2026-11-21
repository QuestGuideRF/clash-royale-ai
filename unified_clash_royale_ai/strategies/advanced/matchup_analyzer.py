from ...data .cards_database import get_card_info ,get_counter_cards
class MatchupAnalyzer :
    def __init__ (self ):
        self .matchup_cache ={}
    def analyze_matchup (self ,our_deck ,opponent_deck ):
        analysis ={
        'advantage_score':0 ,
        'our_threats':[],
        'their_threats':[],
        'our_counters':{},
        'their_counters':{},
        'key_interactions':[],
        'strategy_tips':[]
        }
        for their_card in opponent_deck :
            their_info =get_card_info (their_card )
            if not their_info :
                continue
            our_counters =[]
            for our_card in our_deck :
                if our_card in get_counter_cards (their_card ):
                    our_counters .append (our_card )
            if our_counters :
                analysis ['our_counters'][their_card ]=our_counters
            else :
                analysis ['their_threats'].append ({
                'card':their_card ,
                'danger_level':'high',
                'no_direct_counter':True
                })
        for our_card in our_deck :
            our_info =get_card_info (our_card )
            if not our_info :
                continue
            their_counters =[]
            for their_card in opponent_deck :
                if their_card in get_counter_cards (our_card ):
                    their_counters .append (their_card )
            if their_counters :
                analysis ['their_counters'][our_card ]=their_counters
            else :
                analysis ['our_threats'].append ({
                'card':our_card ,
                'threat_level':'high',
                'no_counter_in_opponent':True
                })
        our_advantages =len (analysis ['our_threats'])
        their_advantages =len (analysis ['their_threats'])
        analysis ['advantage_score']=(our_advantages -their_advantages )*15
        analysis ['advantage_score']=max (-100 ,min (100 ,analysis ['advantage_score']))
        analysis ['key_interactions']=self ._find_key_interactions (our_deck ,opponent_deck )
        analysis ['strategy_tips']=self ._generate_strategy_tips (analysis ,our_deck ,opponent_deck )
        return analysis
    def _find_key_interactions (self ,our_deck ,opponent_deck ):
        interactions =[]
        win_conditions =['hog_rider','giant','golem','balloon','xbow',
        'mortar','goblin_barrel','graveyard','ram_rider']
        for wc in win_conditions :
            if wc in our_deck :
                for their_card in opponent_deck :
                    if their_card in get_counter_cards (wc ):
                        interactions .append ({
                        'type':'win_condition_vs_counter',
                        'our_card':wc ,
                        'their_card':their_card ,
                        'note':f"Будьте осторожны с {wc }, у них есть {their_card }"
                        })
        spells =['fireball','lightning','rocket','poison','arrows','the_log']
        spell_targets =['musketeer','wizard','witch','electro_wizard',
        'princess','magic_archer','hunter']
        for spell in spells :
            if spell in our_deck :
                targets =[c for c in opponent_deck if c in spell_targets ]
                if len (targets )>=2 :
                    interactions .append ({
                    'type':'spell_value',
                    'our_card':spell ,
                    'targets':targets ,
                    'note':f"Ждите хорошего {spell }, у них много целей"
                    })
        return interactions
    def _generate_strategy_tips (self ,analysis ,our_deck ,opponent_deck ):
        tips =[]
        if analysis ['advantage_score']>30 :
            tips .append ("У вас хороший матчап. Играйте агрессивно после защиты.")
        elif analysis ['advantage_score']<-30 :
            tips .append ("Сложный матчап. Играйте осторожно, ждите их ошибок.")
        else :
            tips .append ("Равный матчап. Победит тот, кто лучше играет.")
        if analysis ['their_threats']:
            threat_cards =[t ['card']for t in analysis ['their_threats']]
            tips .append (f"Главные угрозы противника: {', '.join (threat_cards )}")
        if analysis ['our_threats']:
            our_threat_cards =[t ['card']for t in analysis ['our_threats']]
            tips .append (f"Используйте ваши угрозы: {', '.join (our_threat_cards )}")
        if 'golem'in opponent_deck :
            tips .append ("Против Golem: атакуйте противоположную сторону при его размещении")
        if 'xbow'in opponent_deck or 'mortar'in opponent_deck :
            tips .append ("Против Siege: не давайте им заблокировать ваши башни")
        if 'goblin_barrel'in opponent_deck :
            tips .append ("Держите Log/Arrows/Tornado для Goblin Barrel")
        return tips
    def get_matchup_rating (self ,our_deck ,opponent_deck ):
        analysis =self .analyze_matchup (our_deck ,opponent_deck )
        return (analysis ['advantage_score']+100 )/2
    def find_best_deck_against (self ,opponent_deck ,available_decks ):
        best_deck =None
        best_rating =0
        for deck in available_decks :
            rating =self .get_matchup_rating (deck ,opponent_deck )
            if rating >best_rating :
                best_rating =rating
                best_deck =deck
        return {
        'deck':best_deck ,
        'rating':best_rating ,
        'analysis':self .analyze_matchup (best_deck ,opponent_deck )if best_deck else None
        }
    def get_archetype_matchups (self ):
        archetypes =['beatdown','cycle','control','bridge_spam','siege','bait']
        matchup_table ={}
        matchup_data ={
        ('beatdown','cycle'):45 ,
        ('beatdown','control'):55 ,
        ('beatdown','bridge_spam'):40 ,
        ('beatdown','siege'):60 ,
        ('beatdown','bait'):50 ,
        ('cycle','control'):45 ,
        ('cycle','bridge_spam'):55 ,
        ('cycle','siege'):50 ,
        ('cycle','bait'):45 ,
        ('control','bridge_spam'):55 ,
        ('control','siege'):40 ,
        ('control','bait'):55 ,
        ('bridge_spam','siege'):60 ,
        ('bridge_spam','bait'):50 ,
        ('siege','bait'):45 ,
        }
        for arch in archetypes :
            matchup_table [arch ]={}
            for other in archetypes :
                if arch ==other :
                    matchup_table [arch ][other ]=50
                elif (arch ,other )in matchup_data :
                    matchup_table [arch ][other ]=matchup_data [(arch ,other )]
                elif (other ,arch )in matchup_data :
                    matchup_table [arch ][other ]=100 -matchup_data [(other ,arch )]
                else :
                    matchup_table [arch ][other ]=50
        return matchup_table