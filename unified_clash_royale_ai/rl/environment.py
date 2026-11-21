import numpy as np
import os
import sys
try :
    from gym import Env
    from gym .spaces import Discrete ,Box ,Dict
except ImportError :
    class Env :
        pass
    class Discrete :
        def __init__ (self ,n ):
            self .n =n
    class Box :
        def __init__ (self ,low ,high ,shape ,dtype ):
            self .low =low
            self .high =high
            self .shape =shape
            self .dtype =dtype
    class Dict :
        def __init__ (self ,spaces ):
            self .spaces =spaces
class ClashRoyaleEnvironment (Env ):
    def __init__ (self ,screen_capture ,game_state ,action_executor ):
        self .screen_capture =screen_capture
        self .game_state =game_state
        self .action_executor =action_executor
        self .action_space =Dict ({
        "card_choice":Discrete (5 ),
        "position":Box (
        low =np .array ([45 ,150 ]),
        high =np .array ([405 ,600 ]),
        shape =(2 ,),
        dtype =int
        )
        })
        self .observation_space =Dict ({
        "image":Box (low =0 ,high =1 ,shape =(208 ,160 ,1 ),dtype =float ),
        "features":Box (low =0 ,high =1 ,shape =(164 ,),dtype =float )
        })
    def get_state (self ,processed_image ):
        image_state =processed_image
        feature_state =np .random .rand (164 ).astype (np .float32 )
        return [image_state ,feature_state ]
    def step (self ,action ):
        card_choice =action [0 ][0 ]if isinstance (action [0 ],np .ndarray )else action [0 ]
        position =action [1 ]
        if card_choice !=0 :
            pos_range =self .action_space ["position"].high -self .action_space ["position"].low
            real_position =self .action_space ["position"].low +pos_range *position [:2 ]
            card_slot =card_choice -1
            self .action_executor .place_card (card_slot ,real_position )
        screenshot =self .screen_capture .take_screenshot ()
        processed_image =self .screen_capture .process_image (screenshot )
        new_state =self .get_state (processed_image )
        reward =self ._calculate_reward ()
        done =False
        return new_state ,reward ,done
    def _calculate_reward (self ):
        reward =0
        reward +=self .game_state .towers_blue *10
        reward -=self .game_state .towers_red *10
        return reward
    def reset (self ):
        screenshot =self .screen_capture .take_screenshot ()
        processed_image =self .screen_capture .process_image (screenshot )
        return self .get_state (processed_image )