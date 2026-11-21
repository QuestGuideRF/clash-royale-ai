import os
import numpy as np
from datetime import datetime
import json
try :
    import tensorflow as tf
    HAS_TF =True
except ImportError :
    HAS_TF =False
class RLTrainer :
    def __init__ (self ,env ,model_dir ="models/rl"):
        self .env =env
        self .model_dir =model_dir
        self .agent =None
        self .training_history =[]
        os .makedirs (model_dir ,exist_ok =True )
        os .makedirs (os .path .join (model_dir ,'checkpoints'),exist_ok =True )
        os .makedirs (os .path .join (model_dir ,'logs'),exist_ok =True )
    def create_agent (self ,agent_type ='pdqn',**kwargs ):
        from ..rl import PDQNAgent
        if agent_type =='pdqn':
            self .agent =PDQNAgent (self .env ,**kwargs )
        else :
            raise ValueError (f"Неизвестный тип агента: {agent_type }")
        return self .agent
    def train (self ,episodes =1000 ,max_steps =1000 ,save_freq =100 ,
    render =False ,verbose =True ):
        if self .agent is None :
            self .create_agent ()
        timestamp =datetime .now ().strftime ("%Y%m%d_%H%M%S")
        for episode in range (episodes ):
            state =self .env .reset ()
            episode_reward =0
            episode_steps =0
            for step in range (max_steps ):
                action =self .agent .make_action (state ,step )
                next_state ,reward ,done =self .env .step (action )
                self .agent .memorize (state ,action [1 ],reward ,done ,next_state )
                if step %5 ==0 :
                    self .agent .replay (1 )
                state =next_state
                episode_reward +=reward
                episode_steps +=1
                if done :
                    break
            self .agent .on_episode_end ()
            self .training_history .append ({
            'episode':episode ,
            'reward':episode_reward ,
            'steps':episode_steps ,
            'epsilon':self .agent .epsilon
            })
            if verbose and episode %10 ==0 :
                avg_reward =np .mean ([h ['reward']for h in self .training_history [-100 :]])
                print (f"Episode {episode }/{episodes } | "
                f"Reward: {episode_reward :.2f} | "
                f"Avg(100): {avg_reward :.2f} | "
                f"Epsilon: {self .agent .epsilon :.3f}")
            if episode %save_freq ==0 :
                self .save_checkpoint (episode ,timestamp )
        self .save_model (timestamp )
        self .save_history (timestamp )
        return self .training_history
    def save_checkpoint (self ,episode ,timestamp ):
        checkpoint_dir =os .path .join (self .model_dir ,'checkpoints',timestamp )
        os .makedirs (checkpoint_dir ,exist_ok =True )
        self .agent .save_weights (os .path .join (checkpoint_dir ,f'checkpoint_{episode }'))
    def save_model (self ,timestamp ):
        self .agent .save_weights (os .path .join (self .model_dir ,f'rl_agent_{timestamp }'))
    def save_history (self ,timestamp ):
        history_path =os .path .join (self .model_dir ,'logs',f'history_{timestamp }.json')
        with open (history_path ,'w')as f :
            json .dump (self .training_history ,f )
    def load_model (self ,model_path ):
        if self .agent is None :
            self .create_agent ()
        self .agent .load_weights (model_path )
    def evaluate (self ,episodes =10 ):
        total_rewards =[]
        for episode in range (episodes ):
            state =self .env .reset ()
            episode_reward =0
            done =False
            while not done :
                action =self .agent .make_action (state ,0 ,noise =False )
                next_state ,reward ,done =self .env .step (action )
                state =next_state
                episode_reward +=reward
            total_rewards .append (episode_reward )
        return {
        'mean_reward':np .mean (total_rewards ),
        'std_reward':np .std (total_rewards ),
        'min_reward':np .min (total_rewards ),
        'max_reward':np .max (total_rewards )
        }