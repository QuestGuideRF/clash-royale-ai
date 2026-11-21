import json
import os
from typing import Dict ,List ,Optional ,Tuple
from collections import defaultdict
class OpponentPatterns :
    def __init__ (self ,data_file :str ="data/opponent_patterns.json"):
        self .data_file =data_file
        self .data =self ._load_data ()
        self .current_match ={
        'plays':[],
        'patterns_detected':[]
        }
    def _load_data (self )->Dict :
        if os .path .exists (self .data_file ):
            with open (self .data_file ,'r',encoding ='utf-8')as f :
                return json .load (f )
        return {
        'patterns':{},
        'reactions':{},
        'opening_plays':{},
        'closing_plays':{}
        }
    def _save_data (self ):
        os .makedirs (os .path .dirname (self .data_file )or '.',exist_ok =True )
        with open (self .data_file ,'w',encoding ='utf-8')as f :
            json .dump (self .data ,f ,indent =2 ,ensure_ascii =False )
    def record_opponent_play (self ,card :str ,position :Tuple [int ,int ],
    game_time :int ,our_elixir :int ,
    our_last_play :str =None ):
        play ={
        'card':card ,
        'position':position ,
        'game_time':game_time ,
        'our_elixir':our_elixir ,
        'our_last_play':our_last_play
        }
        self .current_match ['plays'].append (play )
        if our_last_play :
            reaction_key =f"{our_last_play }_{card }"
            if reaction_key not in self .data ['reactions']:
                self .data ['reactions'][reaction_key ]={
                'our_play':our_last_play ,
                'opponent_response':card ,
                'count':0
                }
            self .data ['reactions'][reaction_key ]['count']+=1
        if game_time >170 :
            if card not in self .data ['opening_plays']:
                self .data ['opening_plays'][card ]=0
            self .data ['opening_plays'][card ]+=1
        self ._analyze_patterns ()
    def _analyze_patterns (self ):
        plays =self .current_match ['plays']
        if len (plays )<2 :
            return
        last_two =[plays [-2 ]['card'],plays [-1 ]['card']]
        pattern_key ='_'.join (last_two )
        if pattern_key not in self .data ['patterns']:
            self .data ['patterns'][pattern_key ]={
            'sequence':last_two ,
            'count':0
            }
        self .data ['patterns'][pattern_key ]['count']+=1
        if len (plays )>=4 :
            recent_cards =[p ['card']for p in plays [-4 :]]
            for i in range (len (recent_cards )-1 ):
                for j in range (i +2 ,len (recent_cards )):
                    if recent_cards [i ]==recent_cards [j ]:
                        pattern =recent_cards [i :j ]
                        self .current_match ['patterns_detected'].append ({
                        'pattern':pattern ,
                        'position':len (plays )
                        })
    def predict_next_play (self )->Optional [Dict ]:
        if not self .current_match ['plays']:
            if self .data ['opening_plays']:
                most_common =max (
                self .data ['opening_plays'].items (),
                key =lambda x :x [1 ]
                )
                total =sum (self .data ['opening_plays'].values ())
                return {
                'predicted_card':most_common [0 ],
                'confidence':most_common [1 ]/total ,
                'reason':'Самое распространенное открытие'
                }
            return None
        last_card =self .current_match ['plays'][-1 ]['card']
        predictions =[]
        for pattern_key ,pattern_data in self .data ['patterns'].items ():
            sequence =pattern_data ['sequence']
            if sequence [0 ]==last_card :
                predictions .append ({
                'card':sequence [1 ],
                'count':pattern_data ['count']
                })
        if predictions :
            predictions .sort (key =lambda x :x ['count'],reverse =True )
            total =sum (p ['count']for p in predictions )
            return {
            'predicted_card':predictions [0 ]['card'],
            'confidence':predictions [0 ]['count']/total ,
            'alternatives':predictions [1 :3 ],
            'reason':f'Pattern after {last_card }'
            }
        return None
    def predict_reaction (self ,our_card :str )->Optional [Dict ]:
        reactions =[]
        for key ,data in self .data ['reactions'].items ():
            if data ['our_play']==our_card :
                reactions .append ({
                'response':data ['opponent_response'],
                'count':data ['count']
                })
        if reactions :
            reactions .sort (key =lambda x :x ['count'],reverse =True )
            total =sum (r ['count']for r in reactions )
            return {
            'predicted_response':reactions [0 ]['response'],
            'confidence':reactions [0 ]['count']/total ,
            'alternatives':reactions [1 :3 ]
            }
        return None
    def get_opponent_tendencies (self )->Dict :
        if not self .current_match ['plays']:
            return {}
        plays =self .current_match ['plays']
        positions =defaultdict (list )
        for play in plays :
            positions [play ['card']].append (play ['position'])
        preferred_positions ={}
        for card ,pos_list in positions .items ():
            if pos_list :
                avg_x =sum (p [0 ]for p in pos_list )/len (pos_list )
                avg_y =sum (p [1 ]for p in pos_list )/len (pos_list )
                side ='left'if avg_x <240 else 'right'if avg_x >240 else 'center'
                depth ='aggressive'if avg_y <400 else 'defensive'
                preferred_positions [card ]={
                'side':side ,
                'depth':depth ,
                'avg_position':(int (avg_x ),int (avg_y ))
                }
        early_plays =[p for p in plays if p ['game_time']>150 ]
        aggression ='aggressive'if len (early_plays )>3 else 'passive'
        return {
        'positions':preferred_positions ,
        'playstyle':aggression ,
        'total_plays':len (plays ),
        'patterns_detected':len (self .current_match ['patterns_detected'])
        }
    def end_match (self ):
        if self .current_match ['plays']:
            last_plays =self .current_match ['plays'][-3 :]
            for play in last_plays :
                card =play ['card']
                if card not in self .data ['closing_plays']:
                    self .data ['closing_plays'][card ]=0
                self .data ['closing_plays'][card ]+=1
        self ._save_data ()
        self .current_match ={
        'plays':[],
        'patterns_detected':[]
        }
    def generate_report (self )->str :
        report =[]
        report .append ("="*60 )
        report .append ("ПАТТЕРНЫ ПРОТИВНИКА")
        report .append ("="*60 )
        tendencies =self .get_opponent_tendencies ()
        report .append (f"\nТекущий матч:")
        report .append (f"  Ходов противника: {tendencies .get ('total_plays',0 )}")
        report .append (f"  Стиль игры: {tendencies .get ('playstyle','unknown')}")
        report .append (f"  Паттернов обнаружено: {tendencies .get ('patterns_detected',0 )}")
        prediction =self .predict_next_play ()
        if prediction :
            report .append (f"\nПредсказание следующего хода:")
            report .append (f"  Карта: {prediction ['predicted_card']}")
            report .append (f"  Уверенность: {prediction ['confidence']*100 :.1f}%")
        if self .data ['opening_plays']:
            report .append ("\nПопулярные opening plays:")
            sorted_openings =sorted (
            self .data ['opening_plays'].items (),
            key =lambda x :x [1 ],
            reverse =True
            )[:5 ]
            for card ,count in sorted_openings :
                report .append (f"  {card }: {count }")
        return "\n".join (report )