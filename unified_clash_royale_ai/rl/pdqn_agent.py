import numpy as np
import os
import sys
try :
    import tensorflow as tf
except ImportError :
    tf =None
sys .path .insert (0 ,os .path .dirname (os .path .dirname (os .path .abspath (__file__ ))))
from unified_clash_royale_ai .rl .utils import MemoryBuffer ,OUActionNoise
from unified_clash_royale_ai .config import (
DQN_LEARNING_RATE ,DQN_DISCOUNT_FACTOR ,DQN_BATCH_SIZE ,DQN_BUFFER_SIZE ,
DQN_EPSILON_START ,DQN_EPSILON_MIN ,DQN_EPSILON_DECAY
)
class PDQNAgent :
    def __init__ (self ,env ,batch_size =None ,epsilon =None ,eps_decay =None ,eps_min =None ):
        self .env =env
        self .batch_size =batch_size or DQN_BATCH_SIZE
        self .epsilon =epsilon or DQN_EPSILON_START
        self .eps_decay =eps_decay or DQN_EPSILON_DECAY
        self .eps_min =eps_min or DQN_EPSILON_MIN
        self .discount_factor =DQN_DISCOUNT_FACTOR
        self .buffer =MemoryBuffer (DQN_BUFFER_SIZE ,with_per =False )
        self .noise =OUActionNoise (size =8 )
        self .step_count =0
        print ("PDQN Agent инициализирован (упрощенная версия)")
    def make_action (self ,state ,step =None ,noise =True ):
        self .step_count =step or self .step_count +1
        if np .random .uniform ()<self .epsilon :
            return (np .array ([0 ]),np .zeros (8 ))
        else :
            card_choice =np .random .randint (1 ,5 )
            position =np .random .uniform (0 ,1 ,8 )
            if noise :
                position +=self .noise .generate (self .step_count )
                position =np .clip (position ,0 ,1 )
            return (np .array ([card_choice ]),position )
    def memorize (self ,obs ,act ,reward ,done ,new_obs ):
        self .buffer .memorize (
        obs [0 ],obs [1 ],act ,reward ,done ,
        new_obs [0 ],new_obs [1 ],error =None
        )
    def replay (self ,replay_num ):
        if self .buffer .size ()<=self .batch_size :
            return
        if self .epsilon >self .eps_min :
            self .epsilon -=self .eps_decay *replay_num
            self .epsilon =max (self .epsilon ,self .eps_min )
    def on_episode_end (self ):
        if self .epsilon >self .eps_min :
            self .epsilon -=self .eps_decay
            self .epsilon =max (self .epsilon ,self .eps_min )
    def save_weights (self ,path ):
        print (f"Weights would be saved to {path }")
    def load_weights (self ,path ):
        print (f"Weights would be loaded from {path }")