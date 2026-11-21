from typing import List ,Tuple ,Dict ,Optional
class PlacementGuide :
    POSITIONS ={
    'center_back':(0.5 ,0.15 ),
    'left_back':(0.25 ,0.15 ),
    'right_back':(0.75 ,0.15 ),
    'center_mid':(0.5 ,0.35 ),
    'left_mid':(0.25 ,0.35 ),
    'right_mid':(0.75 ,0.35 ),
    'bridge_left':(0.25 ,0.5 ),
    'bridge_right':(0.75 ,0.5 ),
    'anti_building':(0.5 ,0.45 ),
    'princess_left':(0.12 ,0.35 ),
    'princess_right':(0.88 ,0.35 ),
    'king_tower':(0.5 ,0.08 ),
    }
    CARD_PLACEMENTS ={
    'golem':{
    'offensive':['center_back','left_back','right_back'],
    'default':'center_back',
    'notes':'Всегда размещать сзади для накопления эликсира'
    },
    'giant':{
    'offensive':['center_back','left_back','right_back'],
    'default':'center_back',
    'notes':'Размещать сзади, можно ближе если контратака'
    },
    'pekka':{
    'offensive':['center_back'],
    'defensive':['center_mid','left_mid','right_mid'],
    'default':'center_mid',
    'notes':'Лучше использовать для защиты и контратаки'
    },
    'mega_knight':{
    'offensive':['bridge_left','bridge_right'],
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'При защите размещать так, чтобы прыгнул на войска'
    },
    'hog_rider':{
    'offensive':['bridge_left','bridge_right'],
    'default':'bridge_left',
    'notes':'Всегда у моста, можно pig push у реки'
    },
    'balloon':{
    'offensive':['bridge_left','bridge_right'],
    'default':'bridge_left',
    'notes':'За танком или когда нет защиты'
    },
    'ram_rider':{
    'offensive':['bridge_left','bridge_right'],
    'default':'bridge_right',
    'notes':'У моста, может снейрить войска'
    },
    'xbow':{
    'offensive':['anti_building'],
    'defensive':['center_mid'],
    'default':'anti_building',
    'notes':'Offensive X-Bow - 4 тайла от реки по центру'
    },
    'mortar':{
    'offensive':['anti_building'],
    'defensive':['center_mid'],
    'default':'anti_building',
    'notes':'Аналогично X-Bow'
    },
    'goblin_barrel':{
    'offensive':['princess_left','princess_right','king_tower'],
    'default':'princess_left',
    'notes':'На башню, можно трикшоты'
    },
    'graveyard':{
    'offensive':['princess_left','princess_right'],
    'default':'princess_left',
    'notes':'На башню, с танком впереди'
    },
    'musketeer':{
    'offensive':['center_back','left_back','right_back'],
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'Сзади танка или по центру для защиты'
    },
    'wizard':{
    'offensive':['center_back'],
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'Сзади танка для сплеша'
    },
    'electro_wizard':{
    'offensive':['center_back'],
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'Стан при появлении помогает в защите'
    },
    'witch':{
    'offensive':['center_back'],
    'defensive':['center_mid'],
    'default':'center_back',
    'notes':'Сзади для накопления скелетов'
    },
    'cannon':{
    'defensive':['anti_building'],
    'default':'anti_building',
    'notes':'4-3 placement для оттягивания'
    },
    'tesla':{
    'defensive':['anti_building'],
    'default':'anti_building',
    'notes':'Центр для максимального coverage'
    },
    'inferno_tower':{
    'defensive':['anti_building'],
    'default':'anti_building',
    'notes':'Центр, но можно сдвинуть против balloon'
    },
    'goblin_hut':{
    'defensive':['left_back','right_back'],
    'default':'left_back',
    'notes':'Сзади для постоянного давления'
    },
    'tombstone':{
    'defensive':['center_mid','anti_building'],
    'default':'center_mid',
    'notes':'Для отвлечения prince/pekka'
    },
    'fireball':{
    'notes':'На группу войск или башню с низким HP'
    },
    'lightning':{
    'notes':'На 3 дорогих цели или inferno'
    },
    'rocket':{
    'notes':'На elixir collector или для финиша'
    },
    'arrows':{
    'notes':'На орду миньонов, принцессу, бочку гоблинов'
    },
    'the_log':{
    'notes':'На наземные swarm или отталкивание'
    },
    'zap':{
    'notes':'На инферно, искра, летучая мышь/скелет'
    },
    'tornado':{
    'notes':'Активация king tower или группировка'
    },
    'skeleton_army':{
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'Окружить войско противника'
    },
    'minion_horde':{
    'offensive':['bridge_left','bridge_right'],
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'За танком или для DPS'
    },
    'goblin_gang':{
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'Универсальная защита'
    },
    'ice_spirit':{
    'default':'center_mid',
    'notes':'Для цикла или freeze эффекта'
    },
    'skeletons':{
    'default':'center_mid',
    'notes':'Distraction для pekka/prince'
    },
    'ice_golem':{
    'offensive':['bridge_left','bridge_right'],
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'Кайтинг или мини-танки'
    },
    'knight':{
    'offensive':['bridge_left','bridge_right'],
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'Универсальный мини танк'
    },
    'valkyrie':{
    'offensive':['center_back'],
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'Сплеш урон, хороша против swarm'
    },
    'mini_pekka':{
    'offensive':['bridge_left','bridge_right'],
    'defensive':['center_mid'],
    'default':'center_mid',
    'notes':'Tank killer, быстрый урон'
    }
    }
    def __init__ (self ):
        pass
    def get_optimal_position (self ,card_name :str ,situation :str ='default')->Tuple [float ,float ]:
        card_name =card_name .lower ().replace (' ','_')
        if card_name not in self .CARD_PLACEMENTS :
            return self .POSITIONS ['center_mid']
        placement =self .CARD_PLACEMENTS [card_name ]
        if situation in placement :
            positions =placement [situation ]
            if isinstance (positions ,list ):
                pos_name =positions [0 ]
            else :
                pos_name =positions
        else :
            pos_name =placement .get ('default','center_mid')
        return self .POSITIONS .get (pos_name ,self .POSITIONS ['center_mid'])
    def get_all_positions (self ,card_name :str )->Dict :
        card_name =card_name .lower ().replace (' ','_')
        if card_name not in self .CARD_PLACEMENTS :
            return {
            'positions':{'default':self .POSITIONS ['center_mid']},
            'notes':'Нет специфических рекомендаций'
            }
        placement =self .CARD_PLACEMENTS [card_name ]
        result ={'positions':{},'notes':placement .get ('notes','')}
        for situation in ['offensive','defensive','default']:
            if situation in placement :
                positions =placement [situation ]
                if isinstance (positions ,list ):
                    result ['positions'][situation ]=[
                    self .POSITIONS .get (p ,self .POSITIONS ['center_mid'])
                    for p in positions
                    ]
                else :
                    result ['positions'][situation ]=self .POSITIONS .get (
                    positions ,self .POSITIONS ['center_mid']
                    )
        return result
    def get_placement_tips (self ,card_name :str )->str :
        card_name =card_name .lower ().replace (' ','_')
        if card_name in self .CARD_PLACEMENTS :
            return self .CARD_PLACEMENTS [card_name ].get ('notes','Нет советов')
        return 'Нет специфических советов для этой карты'
    def convert_to_screen_coords (self ,normalized_pos :Tuple [float ,float ],
    screen_width :int ,screen_height :int ,
    battlefield_region :Tuple [int ,int ,int ,int ])->Tuple [int ,int ]:
        x1 ,y1 ,x2 ,y2 =battlefield_region
        screen_x =int (x1 +(x2 -x1 )*normalized_pos [0 ])
        screen_y =int (y1 +(y2 -y1 )*normalized_pos [1 ])
        return (screen_x ,screen_y )