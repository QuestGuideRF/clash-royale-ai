import os
MODEL_DIR ="models"
CARD_RECOGNITION_MODEL =os .path .join (MODEL_DIR ,"card_recognition","testNet.model")
CARD_PLACEMENT_MODEL =os .path .join (MODEL_DIR ,"card_recognition","testNet2.model")
YOLO_MODEL =os .path .join (MODEL_DIR ,"yolo","best.pt")
VAE_MODEL =os .path .join (MODEL_DIR ,"vae","vae_weights.h5")
DQN_MODEL =os .path .join (MODEL_DIR ,"dqn","dqn_weights.h5")
SCREEN_WIDTH =1920
SCREEN_HEIGHT =1080
GAME_MON ={'top':30 ,'left':0 ,'width':480 ,'height':830 }
VAE_INPUT_DIM =(208 ,160 ,1 )
VAE_Z_DIM =80
VAE_CONV_FILTERS =[128 ,64 ,64 ,128 ]
VAE_CONV_KERNEL_SIZES =[4 ,4 ,4 ,4 ]
VAE_CONV_STRIDES =[2 ,2 ,2 ,2 ]
VAE_CONV_T_FILTERS =[128 ,64 ,64 ,1 ]
VAE_CONV_T_KERNEL_SIZES =[4 ,4 ,4 ,4 ]
VAE_CONV_T_STRIDES =[2 ,2 ,2 ,2 ]
DQN_LEARNING_RATE =1e-3
DQN_DISCOUNT_FACTOR =0.99
DQN_BATCH_SIZE =32
DQN_BUFFER_SIZE =10000
DQN_EPSILON_START =0.95
DQN_EPSILON_MIN =0.3
DQN_EPSILON_DECAY =0.05
ELIXIR_COOLDOWN_NORMAL =2.8
ELIXIR_COOLDOWN_DOUBLE =1.4
ELIXIR_COOLDOWN_OVERTIME =0.9
TILE_SIZE =25
CARD_SLOTS_POSITIONS =[
(177 ,913 ),(277 ,913 ),(377 ,913 ),(477 ,913 )
]
BLUE_MIDDLE_COORDS =(265 ,560 )
BLUE_BRIDGE_COORDS ={
"left":(128 ,438 ),
"right":(419 ,457 )
}
BLUE_BACK_COORDS ={
"left":(47 ,750 ),
"right":(502 ,751 )
}
WIN_CONDITIONS =["ally_prince","ally_giant","ally_mini_pekka"]
CYCLE_CARDS =["ally_archer","ally_spear_goblin","ally_goblin","ally_knight"]
BUILDINGS =["ally_goblin_cage","ally_goblin_hut"]
SUPPORT_CARDS =["ally_archer","ally_minion","ally_spear_goblin","ally_goblin"]
CARD_COSTS ={
"ally_knight":3 ,
"ally_archer":3 ,
"ally_prince":5 ,
"ally_goblin":2 ,
"ally_spear_goblin":2 ,
"ally_giant":5 ,
"ally_mini_pekka":4 ,
"ally_minion":3 ,
"ally_arrow":3 ,
"ally_fireball":4 ,
"ally_goblin_cage":4 ,
"ally_musketeer":4 ,
"ally_goblin_hut":5
}