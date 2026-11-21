from ..data .cards_database import get_card_info ,get_counter_cards
class ErrorAnalyzer :
    def __init__ (self ):
        self .error_types ={
        'elixir_leak':'Утечка эликсира',
        'bad_placement':'Плохое размещение',
        'wrong_card':'Неправильный выбор карты',
        'early_aggression':'Преждевременная агрессия',
        'no_defense':'Отсутствие защиты',
        'overcommit':'Чрезмерная агрессия',
        'spell_miss':'Промах заклинанием',
        'bad_trade':'Плохой обмен эликсиром'
        }
    def analyze_replay (self ,replay ):
        errors =[]
        for i ,action in enumerate (replay .actions ):
            state =replay .get_state_at_frame (action .get ('frame_id',0 ))
            errors .extend (self ._check_elixir_management (action ,state ,replay ))
            errors .extend (self ._check_card_choice (action ,state ,replay ))
            errors .extend (self ._check_placement (action ,state ,replay ))
            errors .extend (self ._check_timing (action ,state ,replay ,i ))
        errors .extend (self ._analyze_overall_strategy (replay ))
        return errors
    def _check_elixir_management (self ,action ,state ,replay ):
        errors =[]
        if state :
            game_state =state .get ('state',{})
            elixir =game_state .get ('elixir_blue',0 )
            if elixir >=10 and not action .get ('action'):
                errors .append ({
                'type':'elixir_leak',
                'severity':'medium',
                'frame_id':action .get ('frame_id'),
                'description':'Эликсир достиг максимума без использования',
                'recommendation':'Играйте карты, чтобы не терять эликсир'
                })
        return errors
    def _check_card_choice (self ,action ,state ,replay ):
        errors =[]
        action_data =action .get ('action',{})
        if not action_data :
            return errors
        card_played =action_data .get ('card')
        if not card_played :
            return errors
        card_info =get_card_info (card_played )
        if not card_info :
            return errors
        if state :
            game_state =state .get ('state',{})
        return errors
    def _check_placement (self ,action ,state ,replay ):
        errors =[]
        action_data =action .get ('action',{})
        if not action_data :
            return errors
        position =action_data .get ('position')
        card_played =action_data .get ('card')
        if not position or not card_played :
            return errors
        card_info =get_card_info (card_played )
        if not card_info :
            return errors
        tags =card_info .get ('tags',[])
        if 'tank'in tags and position [1 ]<450 :
            errors .append ({
            'type':'bad_placement',
            'severity':'medium',
            'frame_id':action .get ('frame_id'),
            'description':f'Танк {card_played } размещен слишком близко к мосту',
            'recommendation':'Размещайте танков сзади для накопления эликсира'
            })
        return errors
    def _check_timing (self ,action ,state ,replay ,action_index ):
        errors =[]
        if state :
            game_state =state .get ('state',{})
            chrono =game_state .get ('chrono',180 )
            elixir =game_state .get ('elixir_blue',5 )
            if chrono >170 and elixir <8 :
                action_data =action .get ('action',{})
                if action_data :
                    card_played =action_data .get ('card')
                    card_info =get_card_info (card_played )if card_played else None
                    if card_info and 'win_condition'in card_info .get ('tags',[]):
                        errors .append ({
                        'type':'early_aggression',
                        'severity':'high',
                        'frame_id':action .get ('frame_id'),
                        'description':'Агрессивная игра в начале матча',
                        'recommendation':'Подождите до 10 эликсира перед первой атакой'
                        })
        return errors
    def _analyze_overall_strategy (self ,replay ):
        errors =[]
        cards_played ={}
        for action in replay .actions :
            action_data =action .get ('action',{})
            card =action_data .get ('card')
            if card :
                cards_played [card ]=cards_played .get (card ,0 )+1
        total_plays =sum (cards_played .values ())
        if total_plays >0 :
            for card ,count in cards_played .items ():
                if count /total_plays >0.4 :
                    errors .append ({
                    'type':'overcommit',
                    'severity':'low',
                    'description':f'Карта {card } играется слишком часто ({count }/{total_plays })',
                    'recommendation':'Разнообразьте использование карт'
                    })
        return errors
    def get_error_summary (self ,errors ):
        summary ={
        'total_errors':len (errors ),
        'by_type':{},
        'by_severity':{'high':0 ,'medium':0 ,'low':0 }
        }
        for error in errors :
            error_type =error .get ('type','unknown')
            severity =error .get ('severity','low')
            if error_type not in summary ['by_type']:
                summary ['by_type'][error_type ]=0
            summary ['by_type'][error_type ]+=1
            summary ['by_severity'][severity ]+=1
        return summary