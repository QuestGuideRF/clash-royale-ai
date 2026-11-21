import tkinter as tk
from tkinter import ttk ,messagebox
import threading
import time
from PIL import Image ,ImageTk
import os
class ClashRoyaleGUI :
    def __init__ (self ,ai_controller =None ):
        self .ai_controller =ai_controller
        self .running =False
        self .root =None
    def create_window (self ):
        self .root =tk .Tk ()
        self .root .title ("🎮 Искусственный интеллект Clash Royale — унифицированное издание")
        self .root .geometry ("800x600")
        self .root .configure (bg ='#1a1a2e')
        self .setup_styles ()
        self .create_header ()
        self .create_opponent_panel ()
        self .create_game_state_panel ()
        self .create_control_panel ()
        self .create_log_panel ()
        self .create_status_bar ()
        return self .root
    def setup_styles (self ):
        style =ttk .Style ()
        style .theme_use ('clam')
        self .colors ={
        'bg_dark':'#1a1a2e',
        'bg_medium':'#16213e',
        'bg_light':'#0f3460',
        'accent':'#e94560',
        'accent_light':'#ff6b6b',
        'text':'#аааааа',
        'text_dim':'#а0а0а0',
        'elixir':'#ff69b4',
        'health_green':'#00ff7f',
        'health_red':'#ff4444'
        }
        style .configure ('Dark.TFrame',background =self .colors ['bg_dark'])
        style .configure ('Dark.TLabel',
        background =self .colors ['bg_dark'],
        foreground =self .colors ['text'],
        font =('Следуйте пользовательскому интерфейсу',10 ))
        style .configure ('Header.TLabel',
        background =self .colors ['bg_dark'],
        foreground =self .colors ['accent'],
        font =('Следуйте пользовательскому интерфейсу',14 ,'bold'))
        style .configure ('Accent.TButton',
        background =self .colors ['accent'],
        foreground ='white',
        font =('Следуйте пользовательскому интерфейсу',10 ,'bold'))
    def create_header (self ):
        header_frame =tk .Frame (self .root ,bg =self .colors ['bg_medium'],height =60 )
        header_frame .pack (fill ='x',padx =10 ,pady =10 )
        header_frame .pack_propagate (False )
        title =tk .Label (
        header_frame ,
        text ="🎮 КЛЭШ РОЯЛ ИИ",
        font =('Следуйте пользовательскому интерфейсу',20 ,'bold'),
        bg =self .colors ['bg_medium'],
        fg =self .colors ['accent']
        )
        title .pack (pady =15 )
    def create_opponent_panel (self ):
        opponent_frame =tk .LabelFrame (
        self .root ,
        text ="👤 Карты противника",
        font =('Следуйте пользовательскому интерфейсу',12 ,'bold'),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text'],
        padx =10 ,
        pady =10
        )
        opponent_frame .pack (fill ='x',padx =10 ,pady =5 )
        hand_frame =tk .Frame (opponent_frame ,bg =self .colors ['bg_dark'])
        hand_frame .pack (fill ='x',pady =5 )
        tk .Label (
        hand_frame ,
        text ="В руке:",
        font =('Следуйте пользовательскому интерфейсу',10 ),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text_dim']
        ).pack (side ='left',padx =5 )
        self .opponent_hand_labels =[]
        for i in range (4 ):
            label =tk .Label (
            hand_frame ,
            text ="❓",
            font =('Следуйте пользовательскому интерфейсу',24 ),
            bg =self .colors ['bg_light'],
            fg =self .colors ['text'],
            width =4 ,
            height =2 ,
            relief ='raised'
            )
            label .pack (side ='left',padx =5 )
            self .opponent_hand_labels .append (label )
        upcoming_frame =tk .Frame (opponent_frame ,bg =self .colors ['bg_dark'])
        upcoming_frame .pack (fill ='x',pady =5 )
        tk .Label (
        upcoming_frame ,
        text ="Следующие:",
        font =('Следуйте пользовательскому интерфейсу',10 ),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text_dim']
        ).pack (side ='left',padx =5 )
        self .opponent_upcoming_labels =[]
        for i in range (4 ):
            label =tk .Label (
            upcoming_frame ,
            text ="❓",
            font =('Следуйте пользовательскому интерфейсу',18 ),
            bg =self .colors ['bg_medium'],
            fg =self .colors ['text_dim'],
            width =4 ,
            height =2 ,
            relief ='groove'
            )
            label .pack (side ='left',padx =5 )
            self .opponent_upcoming_labels .append (label )
        elixir_frame =tk .Frame (opponent_frame ,bg =self .colors ['bg_dark'])
        elixir_frame .pack (fill ='x',pady =5 )
        tk .Label (
        elixir_frame ,
        text ="💧 Эликсир:",
        font =('Следуйте пользовательскому интерфейсу',10 ),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text_dim']
        ).pack (side ='left',padx =5 )
        self .opponent_elixir_label =tk .Label (
        elixir_frame ,
        text ="5.0",
        font =('Следуйте пользовательскому интерфейсу',16 ,'bold'),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['elixir']
        )
        self .opponent_elixir_label .pack (side ='left',padx =5 )
    def create_game_state_panel (self ):
        state_frame =tk .LabelFrame (
        self .root ,
        text ="📊 Состояние игры",
        font =('Следуйте пользовательскому интерфейсу',12 ,'bold'),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text'],
        padx =10 ,
        pady =10
        )
        state_frame .pack (fill ='x',padx =10 ,pady =5 )
        towers_frame =tk .Frame (state_frame ,bg =self .colors ['bg_dark'])
        towers_frame .pack (fill ='x',pady =5 )
        tk .Label (
        towers_frame ,
        text ="🔴 Противник:",
        font =('Следуйте пользовательскому интерфейсу',10 ),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text_dim']
        ).pack (side ='left',padx =5 )
        self .enemy_towers_label =tk .Label (
        towers_frame ,
        text ="👑 👑 👑",
        font =('Следуйте пользовательскому интерфейсу',14 ),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['health_red']
        )
        self .enemy_towers_label .pack (side ='left',padx =10 )
        tk .Label (
        towers_frame ,
        text ="🔵 Игрок:",
        font =('Следуйте пользовательскому интерфейсу',10 ),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text_dim']
        ).pack (side ='left',padx =20 )
        self .player_towers_label =tk .Label (
        towers_frame ,
        text ="👑 👑 👑",
        font =('Следуйте пользовательскому интерфейсу',14 ),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['health_green']
        )
        self .player_towers_label .pack (side ='left',padx =10 )
        timer_frame =tk .Frame (state_frame ,bg =self .colors ['bg_dark'])
        timer_frame .pack (fill ='x',pady =5 )
        tk .Label (
        timer_frame ,
        text ="⏱️ Время:",
        font =('Следуйте пользовательскому интерфейсу',10 ),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text_dim']
        ).pack (side ='left',padx =5 )
        self .timer_label =tk .Label (
        timer_frame ,
        text ="3:00",
        font =('Следуйте пользовательскому интерфейсу',16 ,'bold'),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text']
        )
        self .timer_label .pack (side ='left',padx =10 )
        self .mode_label =tk .Label (
        timer_frame ,
        text ="⚡ Обычный режим",
        font =('Следуйте пользовательскому интерфейсу',10 ),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['accent_light']
        )
        self .mode_label .pack (side ='left',padx =20 )
    def create_control_panel (self ):
        control_frame =tk .LabelFrame (
        self .root ,
        text ="🎛️ Управление",
        font =('Следуйте пользовательскому интерфейсу',12 ,'bold'),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text'],
        padx =10 ,
        pady =10
        )
        control_frame .pack (fill ='x',padx =10 ,pady =5 )
        buttons_frame =tk .Frame (control_frame ,bg =self .colors ['bg_dark'])
        buttons_frame .pack (fill ='x',pady =5 )
        self .start_button =tk .Button (
        buttons_frame ,
        text ="▶️ Старт",
        font =('Следуйте пользовательскому интерфейсу',11 ,'bold'),
        bg =self .colors ['accent'],
        fg ='white',
        width =12 ,
        command =self .start_ai
        )
        self .start_button .pack (side ='left',padx =5 )
        self .stop_button =tk .Button (
        buttons_frame ,
        text ="⏹️ Стоп",
        font =('Следуйте пользовательскому интерфейсу',11 ,'bold'),
        bg ='#555',
        fg ='white',
        width =12 ,
        command =self .stop_ai ,
        state ='disabled'
        )
        self .stop_button .pack (side ='left',padx =5 )
        mode_frame =tk .Frame (control_frame ,bg =self .colors ['bg_dark'])
        mode_frame .pack (fill ='x',pady =5 )
        tk .Label (
        mode_frame ,
        text ="Режим ИИ:",
        font =('Следуйте пользовательскому интерфейсу',10 ),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text_dim']
        ).pack (side ='left',padx =5 )
        self .mode_var =tk .StringVar (value ='hybrid')
        modes =[('Гибридный','hybrid'),('RL','rl'),('Правила','rule_based')]
        for text ,value in modes :
            rb =tk .Radiobutton (
            mode_frame ,
            text =text ,
            variable =self .mode_var ,
            value =value ,
            font =('Следуйте пользовательскому интерфейсу',10 ),
            bg =self .colors ['bg_dark'],
            fg =self .colors ['text'],
            selectcolor =self .colors ['bg_medium']
            )
            rb .pack (side ='left',padx =10 )
    def create_log_panel (self ):
        log_frame =tk .LabelFrame (
        self .root ,
        text ="📜 Лог действий",
        font =('Следуйте пользовательскому интерфейсу',12 ,'bold'),
        bg =self .colors ['bg_dark'],
        fg =self .colors ['text'],
        padx =10 ,
        pady =10
        )
        log_frame .pack (fill ='both',expand =True ,padx =10 ,pady =5 )
        self .log_text =tk .Text (
        log_frame ,
        font =('Consolas',9 ),
        bg =self .colors ['bg_medium'],
        fg =self .colors ['text'],
        height =8 ,
        state ='disabled'
        )
        self .log_text .pack (fill ='both',expand =True ,pady =5 )
        scrollbar =tk .Scrollbar (self .log_text )
        scrollbar .pack (side ='right',fill ='y')
        self .log_text .config (yscrollcommand =scrollbar .set )
        scrollbar .config (command =self .log_text .yview )
    def create_status_bar (self ):
        status_frame =tk .Frame (self .root ,bg =self .colors ['bg_medium'],height =30 )
        status_frame .pack (fill ='x',side ='bottom')
        status_frame .pack_propagate (False )
        self .status_label =tk .Label (
        status_frame ,
        text ="🟢 Готов к работе",
        font =('Следуйте пользовательскому интерфейсу',9 ),
        bg =self .colors ['bg_medium'],
        fg =self .colors ['text']
        )
        self .status_label .pack (side ='left',padx =10 ,pady =5 )
        self .fps_label =tk .Label (
        status_frame ,
        text ="ФПС: --",
        font =('Следуйте пользовательскому интерфейсу',9 ),
        bg =self .colors ['bg_medium'],
        fg =self .colors ['text_dim']
        )
        self .fps_label .pack (side ='right',padx =10 ,pady =5 )
    def log (self ,message ):
        self .log_text .config (state ='normal')
        timestamp =time .strftime ("%H:%M:%S")
        self .log_text .insert ('end',f"[{timestamp }] {message }\n")
        self .log_text .see ('end')
        self .log_text .config (state ='disabled')
    def update_opponent_hand (self ,cards ):
        card_emojis ={
        'knight':'⚔️','archers':'🏹','giant':'🦣','hog_rider':'🐷',
        'fireball':'🔥','arrows':'➡️','zap':'⚡','minions':'🦇',
        'skeleton':'💀','goblin':'👺','valkyrie':'🪓','wizard':'🧙',
        'prince':'🤴','pekka':'🤖','balloon':'🎈','witch':'🧹',
        'golem':'🗿','poison':'☠️','freeze':'❄️','rage':'😤',
        'unknown':'❓'
        }
        for i ,label in enumerate (self .opponent_hand_labels ):
            if i <len (cards )and cards [i ]!='MysteryCard':
                card =cards [i ].lower ().replace ('ally_','').replace ('enemy_','')
                emoji =card_emojis .get (card ,'🃏')
                label .config (text =emoji )
            else :
                label .config (text ='❓')
    def update_elixir (self ,elixir ):
        self .opponent_elixir_label .config (text =f"{elixir :.1f}")
    def update_towers (self ,player_towers ,enemy_towers ):
        player_str ='👑 '*player_towers +'💔 '*(3 -player_towers )
        enemy_str ='👑 '*enemy_towers +'💔 '*(3 -enemy_towers )
        self .player_towers_label .config (text =player_str .strip ())
        self .enemy_towers_label .config (text =enemy_str .strip ())
    def update_timer (self ,seconds ):
        minutes =seconds //60
        secs =seconds %60
        self .timer_label .config (text =f"{minutes }:{secs :02d}")
        if seconds <=60 :
            self .mode_label .config (text ="⚡⚡ Двойной эликсир!")
        elif seconds <=0 :
            self .mode_label .config (text ="🔥 ОВЕРТАЙМ!")
    def update_fps (self ,fps ):
        self .fps_label .config (text =f"FPS: {fps :.1f}")
    def set_status (self ,status ,color =None ):
        self .status_label .config (text =status )
        if color :
            self .status_label .config (fg =color )
    def start_ai (self ):
        self .running =True
        self .start_button .config (state ='disabled')
        self .stop_button .config (state ='normal')
        self .set_status ("🟡 AI работает...",self .colors ['accent_light'])
        self .log ("AI запущен в режиме: "+self .mode_var .get ())
        if self .ai_controller :
            threading .Thread (
            target =self .ai_controller .run ,
            args =(self .mode_var .get (),),
            daemon =True
            ).start ()
    def stop_ai (self ):
        self .running =False
        self .start_button .config (state ='normal')
        self .stop_button .config (state ='disabled')
        self .set_status ("🔴 AI остановлен",self .colors ['text_dim'])
        self .log ("AI остановлен")
    def run (self ):
        if self .root is None :
            self .create_window ()
        self .root .mainloop ()