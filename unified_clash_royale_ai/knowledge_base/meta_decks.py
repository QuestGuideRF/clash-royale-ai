from typing import List ,Dict ,Optional
from datetime import datetime
class MetaDecksDatabase :
    META_DECKS =[
    {
    'id':'hog_2.6',
    'name':'Боров 2.6 Цикл',
    'archetype':'cycle',
    'cards':['hog_rider','musketeer','ice_spirit','skeletons',
    'cannon','fireball','the_log','ice_golem'],
    'avg_cost':2.6 ,
    'difficulty':'expert',
    'playstyle':'Быстрый цикл, постоянное давление Hog Rider',
    'strengths':['Быстрый цикл','Outcycle контры','Повреждение стружки'],
    'weaknesses':['Beatdown','Много splash'],
    'tips':[
    'Играйте Hog когда у противника нет контры в руке',
    'Используйте Ice Golem для защиты Musketeer',
    'Cannon - главная защита, размещайте правильно'
    ]
    },
    {
    'id':'golem_beatdown',
    'name':'Избиение Голема',
    'archetype':'beatdown',
    'cards':['golem','night_witch','baby_dragon','mega_minion',
    'lightning','tornado','tombstone','lumberjack'],
    'avg_cost':4.1 ,
    'difficulty':'medium',
    'playstyle':'Накопление пуша за Golem',
    'strengths':['Огромный push','Сильный late game'],
    'weaknesses':['Адская Башня','Быстрые cycle колоды'],
    'tips':[
    'Ставьте Golem сзади и копите эликсир',
    'Lightning используйте на Inferno/Musketeer',
    'Tornado для группировки под Baby Dragon'
    ]
    },
    {
    'id':'log_bait',
    'name':'Классическая наживка для бревен',
    'archetype':'bait',
    'cards':['goblin_barrel','princess','goblin_gang','ice_spirit',
    'inferno_tower','rocket','the_log','knight'],
    'avg_cost':3.3 ,
    'difficulty':'medium',
    'playstyle':'Журнал приманки и контратака Goblin Barrel',
    'strengths':['Заклинание приманки','Хорошая защита'],
    'weaknesses':['Много spell','Valkyrie'],
    'tips':[
    'Держите Princess и Goblin Gang чтобы bait Log',
    'Rocket для финиша или value',
    'Inferno Tower против танков'
    ]
    },
    {
    'id':'xbow_2.9',
    'name':'X-Лук 2.9',
    'archetype':'siege',
    'cards':['xbow','tesla','archers','ice_spirit',
    'skeletons','fireball','the_log','knight'],
    'avg_cost':2.9 ,
    'difficulty':'expert',
    'playstyle':'Защитный X-Bow и chip damage',
    'strengths':['Контроль','Быстрый цикл'],
    'weaknesses':['Королевский Гигант','Golem','Earthquake'],
    'tips':[
    'Не спешите ставить X-Bow в начале',
    'Tesla - главная защита',
    'Defensive X-Bow если проигрываете'
    ]
    },
    {
    'id':'pekka_bridge_spam',
    'name':'Спам на мосту PEKKA',
    'archetype':'bridge_spam',
    'cards':['pekka','battle_ram','royal_ghost','bandit',
    'electro_wizard','minions','poison','zap'],
    'avg_cost':3.8 ,
    'difficulty':'medium',
    'playstyle':'Давление у моста и контратаки с PEKKA',
    'strengths':['Сильная защита','Быстрые контратаки'],
    'weaknesses':['Bait колоды','Cycle колоды'],
    'tips':[
    'PEKKA только для защиты',
    'Боевой Таран и Бандит на мосту',
    'Яд для роя и кладбища'
    ]
    },
    {
    'id':'lava_loon',
    'name':'Лавовая гагара',
    'archetype':'beatdown',
    'cards':['lava_hound','balloon','mega_minion','minions',
    'tombstone','fireball','zap','skeleton_army'],
    'avg_cost':3.8 ,
    'difficulty':'medium',
    'playstyle':'Воздушный beatdown',
    'strengths':['Сильный air push','Множество авиационных подразделений'],
    'weaknesses':['Очень против воздуха','Адская Башня'],
    'tips':[
    'Лавовая гончая сзади',
    'Воздушный шар для Lava Hound',
    'Зап для Inferno Tower'
    ]
    },
    {
    'id':'miner_wb',
    'name':'Шахтерские стенобои',
    'archetype':'control',
    'cards':['miner','wall_breakers','magic_archer','valkyrie',
    'bomb_tower','fireball','the_log','skeletons'],
    'avg_cost':3.0 ,
    'difficulty':'medium',
    'playstyle':'Chip damage и контроль',
    'strengths':['Многочисленные повреждения чипов','Хорошая защита'],
    'weaknesses':['Beatdown','Сильный air'],
    'tips':[
    'Miner для танкования Wall Breakers',
    'Magic Archer для value',
    'Bomb Tower для splash защиты'
    ]
    },
    {
    'id':'royal_giant_fisherman',
    'name':'Королевский гигантский рыбак',
    'archetype':'beatdown',
    'cards':['royal_giant','fisherman','hunter','electro_wizard',
    'mega_minion','lightning','tornado','skeletons'],
    'avg_cost':3.6 ,
    'difficulty':'medium',
    'playstyle':'Давление Royal Giant с поддержкой',
    'strengths':['Сильный против Siege','Хорошая защита'],
    'weaknesses':['Адская Башня','PEKKA'],
    'tips':[
    'Royal Giant у моста с поддержкой',
    'Fisherman тянет войска к King Tower',
    'Lightning для Inferno'
    ]
    },
    {
    'id':'splashyard',
    'name':'Splashyard',
    'archetype':'control',
    'cards':['graveyard','baby_dragon','tornado','poison',
    'knight','ice_wizard','tombstone','barb_barrel'],
    'avg_cost':3.1 ,
    'difficulty':'hard',
    'playstyle':'Контроль с Graveyard финишами',
    'strengths':['Контроль брызг','Сильная защита'],
    'weaknesses':['Poison в ответ','Очень много'],
    'tips':[
    'Кладбище после танка',
    'Tornado + Baby Dragon для защиты',
    'Яд вместо кладбища'
    ]
    },
    {
    'id':'3m_pump',
    'name':'3 мушкетера Насос',
    'archetype':'beatdown',
    'cards':['three_musketeers','elixir_collector','battle_ram',
    'minion_horde','goblin_gang','miner','fireball','zap'],
    'avg_cost':4.1 ,
    'difficulty':'hard',
    'playstyle':'Преимущество эликсира и сплит-пуш',
    'strengths':['Огромный split push','Заклинание приманки'],
    'weaknesses':['Fireball/Lightning','Тяжелые заклинания'],
    'tips':[
    'Качайте эликсир Pump',
    'Split 3M (1 слева, 2 справа)',
    'Bait Fireball перед 3M'
    ]
    }
    ]
    def __init__ (self ):
        self .decks ={d ['id']:d for d in self .META_DECKS }
    def get_deck (self ,deck_id :str )->Optional [Dict ]:
        return self .decks .get (deck_id )
    def get_all_decks (self )->List [Dict ]:
        return self .META_DECKS
    def get_decks_by_archetype (self ,archetype :str )->List [Dict ]:
        return [d for d in self .META_DECKS if d ['archetype']==archetype ]
    def get_decks_by_card (self ,card_name :str )->List [Dict ]:
        card_name =card_name .lower ().replace (' ','_')
        return [d for d in self .META_DECKS if card_name in d ['cards']]
    def get_decks_by_difficulty (self ,difficulty :str )->List [Dict ]:
        return [d for d in self .META_DECKS if d ['difficulty']==difficulty ]
    def search_similar_deck (self ,cards :List [str ],min_match :int =4 )->List [Dict ]:
        results =[]
        cards_set =set (c .lower ().replace (' ','_')for c in cards )
        for deck in self .META_DECKS :
            deck_cards =set (deck ['cards'])
            matches =len (cards_set &deck_cards )
            if matches >=min_match :
                results .append ({
                'deck':deck ,
                'matches':matches ,
                'match_rate':matches /8
                })
        results .sort (key =lambda x :x ['matches'],reverse =True )
        return results
    def get_tips_for_deck (self ,deck_id :str )->List [str ]:
        deck =self .get_deck (deck_id )
        if deck :
            return deck .get ('tips',[])
        return []
    def get_counter_decks (self ,deck_id :str )->List [str ]:
        deck =self .get_deck (deck_id )
        if not deck :
            return []
        archetype =deck ['archetype']
        counter_archetypes ={
        'beatdown':['cycle','siege'],
        'cycle':['control'],
        'siege':['beatdown'],
        'bridge_spam':['control'],
        'control':['beatdown'],
        'bait':['control']
        }
        counter_types =counter_archetypes .get (archetype ,[])
        counter_decks =[]
        for ct in counter_types :
            counter_decks .extend ([d ['id']for d in self .get_decks_by_archetype (ct )])
        return counter_decks