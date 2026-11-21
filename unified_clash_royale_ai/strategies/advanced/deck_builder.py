from ...data .cards_database import get_card_info ,get_all_cards
class DeckBuilder :
    def __init__ (self ):
        self .archetypes ={
        'beatdown':{
        'description':'Тяжелые танки с поддержкой',
        'required_roles':['tank','support','splash','spell'],
        'avg_cost_range':(3.5 ,4.5 )
        },
        'cycle':{
        'description':'Быстрый цикл карт',
        'required_roles':['win_condition','cycle','spell'],
        'avg_cost_range':(2.6 ,3.2 )
        },
        'control':{
        'description':'Контроль и защита',
        'required_roles':['building','splash','spell','anti_air'],
        'avg_cost_range':(3.2 ,4.0 )
        },
        'bridge_spam':{
        'description':'Агрессивные юниты у моста',
        'required_roles':['bridge_spam','support','spell'],
        'avg_cost_range':(3.0 ,3.8 )
        },
        'siege':{
        'description':'Дальнобойные здания',
        'required_roles':['siege','spell','cycle'],
        'avg_cost_range':(3.0 ,3.5 )
        },
        'bait':{
        'description':'Множество заклинательных целей',
        'required_roles':['bait','spell','win_condition'],
        'avg_cost_range':(3.0 ,3.6 )
        }
        }
    def build_deck (self ,archetype ,preferred_cards =None ,banned_cards =None ):
        if archetype not in self .archetypes :
            raise ValueError (f"Неизвестный архетип: {archetype }")
        archetype_info =self .archetypes [archetype ]
        deck =[]
        if preferred_cards :
            for card in preferred_cards [:4 ]:
                if self ._validate_card (card ,banned_cards ):
                    deck .append (card )
        all_cards =get_all_cards ()
        for role in archetype_info ['required_roles']:
            if len (deck )>=8 :
                break
            card =self ._find_card_for_role (role ,deck ,all_cards ,banned_cards )
            if card :
                deck .append (card )
        while len (deck )<8 :
            card =self ._find_synergy_card (deck ,all_cards ,banned_cards )
            if card :
                deck .append (card )
            else :
                break
        avg_cost =self ._calculate_avg_cost (deck )
        min_cost ,max_cost =archetype_info ['avg_cost_range']
        if avg_cost >max_cost :
            deck =self ._reduce_cost (deck ,max_cost ,all_cards ,banned_cards )
        elif avg_cost <min_cost :
            deck =self ._increase_cost (deck ,min_cost ,all_cards ,banned_cards )
        return {
        'cards':deck ,
        'archetype':archetype ,
        'avg_cost':self ._calculate_avg_cost (deck ),
        'synergy_score':self ._calculate_synergy (deck )
        }
    def _validate_card (self ,card ,banned_cards ):
        if banned_cards and card in banned_cards :
            return False
        return get_card_info (card )is not None
    def _find_card_for_role (self ,role ,current_deck ,all_cards ,banned_cards ):
        for card_name ,card_data in all_cards .items ():
            if card_name in current_deck :
                continue
            if banned_cards and card_name in banned_cards :
                continue
            tags =card_data .get ('tags',[])
            if role in tags :
                return card_name
        return None
    def _find_synergy_card (self ,current_deck ,all_cards ,banned_cards ):
        best_card =None
        best_score =-1
        for card_name ,card_data in all_cards .items ():
            if card_name in current_deck :
                continue
            if banned_cards and card_name in banned_cards :
                continue
            score =self ._card_synergy_score (card_name ,current_deck )
            if score >best_score :
                best_score =score
                best_card =card_name
        return best_card
    def _card_synergy_score (self ,card ,deck ):
        card_info =get_card_info (card )
        if not card_info :
            return 0
        score =0
        card_tags =set (card_info .get ('tags',[]))
        for deck_card in deck :
            deck_card_info =get_card_info (deck_card )
            if not deck_card_info :
                continue
            deck_tags =set (deck_card_info .get ('tags',[]))
            if 'tank'in deck_tags and 'support'in card_tags :
                score +=3
            if 'splash'in card_tags and 'swarm'in deck_tags :
                score +=2
            if 'air'in deck_tags and 'anti_air'in card_tags :
                score +=2
            if 'spell'in card_tags and 'bait'in deck_tags :
                score +=2
        return score
    def _calculate_avg_cost (self ,deck ):
        total_cost =0
        for card in deck :
            info =get_card_info (card )
            if info :
                total_cost +=info .get ('elixir',4 )
        return total_cost /len (deck )if deck else 0
    def _calculate_synergy (self ,deck ):
        total_synergy =0
        for i ,card in enumerate (deck ):
            for other_card in deck [i +1 :]:
                total_synergy +=self ._card_synergy_score (card ,[other_card ])
        return total_synergy
    def _reduce_cost (self ,deck ,target_cost ,all_cards ,banned_cards ):
        while self ._calculate_avg_cost (deck )>target_cost :
            most_expensive =max (
            deck ,
            key =lambda c :get_card_info (c ).get ('elixir',0 )if get_card_info (c )else 0
            )
            card_info =get_card_info (most_expensive )
            if card_info :
                tags =card_info .get ('tags',[])
                role =tags [0 ]if tags else None
                deck .remove (most_expensive )
                cheaper =self ._find_cheaper_card (role ,deck ,all_cards ,banned_cards ,
                card_info .get ('elixir',4 ))
                if cheaper :
                    deck .append (cheaper )
                else :
                    deck .append (most_expensive )
                    break
        return deck
    def _increase_cost (self ,deck ,target_cost ,all_cards ,banned_cards ):
        return deck
    def _find_cheaper_card (self ,role ,deck ,all_cards ,banned_cards ,max_cost ):
        for card_name ,card_data in all_cards .items ():
            if card_name in deck :
                continue
            if banned_cards and card_name in banned_cards :
                continue
            if card_data .get ('elixir',0 )>=max_cost :
                continue
            if role and role in card_data .get ('tags',[]):
                return card_name
        return None
    def suggest_improvements (self ,deck ):
        suggestions =[]
        roles =self ._analyze_roles (deck )
        if not roles .get ('win_condition'):
            suggestions .append ("Добавьте win condition (Hog Rider, Giant, Balloon и т.д.)")
        if not roles .get ('spell'):
            suggestions .append ("Добавьте заклинание (Fireball, Log, Arrows)")
        if not roles .get ('anti_air'):
            suggestions .append ("Добавьте защиту от воздуха (Musketeer, Minions)")
        avg_cost =self ._calculate_avg_cost (deck )
        if avg_cost >4.2 :
            suggestions .append (f"Колода слишком тяжелая (средний кост: {avg_cost :.1f})")
        elif avg_cost <2.8 :
            suggestions .append (f"Колода слишком легкая (средний кост: {avg_cost :.1f})")
        synergy =self ._calculate_synergy (deck )
        if synergy <10 :
            suggestions .append ("Низкая синергия между картами")
        return suggestions
    def _analyze_roles (self ,deck ):
        roles ={}
        for card in deck :
            info =get_card_info (card )
            if info :
                for tag in info .get ('tags',[]):
                    roles [tag ]=True
        return roles
    def get_popular_decks (self ,archetype =None ):
        decks =[
        {
        'name':'Боров 2.6',
        'archetype':'cycle',
        'cards':['hog_rider','musketeer','ice_spirit','skeletons',
        'cannon','fireball','the_log','ice_golem'],
        'avg_cost':2.6
        },
        {
        'name':'Избиение Голема',
        'archetype':'beatdown',
        'cards':['golem','night_witch','baby_dragon','mega_minion',
        'lightning','tornado','tombstone','elixir_collector'],
        'avg_cost':4.1
        },
        {
        'name':'Бревенчатая наживка',
        'archetype':'bait',
        'cards':['goblin_barrel','princess','goblin_gang','ice_spirit',
        'inferno_tower','rocket','the_log','knight'],
        'avg_cost':3.3
        },
        {
        'name':'X-Лук 3.0',
        'archetype':'siege',
        'cards':['xbow','tesla','ice_spirit','skeletons',
        'fireball','the_log','archers','knight'],
        'avg_cost':3.0
        },
        {
        'name':'Мостовой спам',
        'archetype':'bridge_spam',
        'cards':['pekka','battle_ram','royal_ghost','bandit',
        'electro_wizard','minions','poison','zap'],
        'avg_cost':3.8
        }
        ]
        if archetype :
            return [d for d in decks if d ['archetype']==archetype ]
        return decks