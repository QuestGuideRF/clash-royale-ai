import os
import cv2
import numpy as np
class MatchVisualizer :
    def __init__ (self ):
        self .colors ={
        'ally':(0 ,255 ,0 ),
        'enemy':(0 ,0 ,255 ),
        'neutral':(255 ,255 ,0 ),
        'text':(255 ,255 ,255 ),
        'elixir':(255 ,105 ,180 )
        }
    def visualize_frame (self ,frame ,state =None ,action =None ):
        vis_frame =frame .copy ()
        if state :
            self ._draw_game_info (vis_frame ,state )
        if action :
            self ._draw_action (vis_frame ,action )
        return vis_frame
    def _draw_game_info (self ,frame ,state ):
        game_state =state .get ('state',{})
        elixir =game_state .get ('elixir_blue',0 )
        cv2 .putText (
        frame ,f"Elixir: {elixir }",
        (10 ,30 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.7 ,
        self .colors ['elixir'],2
        )
        towers_blue =game_state .get ('towers_blue',3 )
        towers_red =game_state .get ('towers_red',3 )
        cv2 .putText (
        frame ,f"Towers: {towers_blue } - {towers_red }",
        (10 ,60 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.7 ,
        self .colors ['text'],2
        )
        chrono =game_state .get ('chrono',0 )
        minutes =chrono //60
        seconds =chrono %60
        cv2 .putText (
        frame ,f"Time: {minutes }:{seconds :02d}",
        (10 ,90 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.7 ,
        self .colors ['text'],2
        )
    def _draw_action (self ,frame ,action ):
        action_data =action .get ('action',{})
        if action_data :
            cv2 .putText (
            frame ,"ДЕЙСТВИЕ!",
            (frame .shape [1 ]-150 ,30 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.8 ,
            self .colors ['ally'],2
            )
    def create_heatmap (self ,replay ,action_type ='card_play'):
        heatmap =np .zeros ((800 ,480 ),dtype =np .float32 )
        for action in replay .actions :
            action_data =action .get ('action',{})
            if action_data :
                pos =action_data .get ('position',(240 ,400 ))
                if isinstance (pos ,(list ,tuple ))and len (pos )>=2 :
                    x ,y =int (pos [0 ]),int (pos [1 ])
                    if 0 <=x <480 and 0 <=y <800 :
                        cv2 .circle (heatmap ,(x ,y ),30 ,1 ,-1 )
        heatmap =cv2 .normalize (heatmap ,None ,0 ,255 ,cv2 .NORM_MINMAX )
        heatmap =heatmap .astype (np .uint8 )
        heatmap_colored =cv2 .applyColorMap (heatmap ,cv2 .COLORMAP_JET )
        return heatmap_colored
    def create_timeline_visualization (self ,replay ,width =1200 ,height =200 ):
        timeline =np .zeros ((height ,width ,3 ),dtype =np .uint8 )
        timeline [:]=(30 ,30 ,30 )
        if not replay .actions :
            return timeline
        if replay .states :
            first_time =replay .states [0 ].get ('timestamp',0 )
            last_time =replay .states [-1 ].get ('timestamp',first_time +180 )
            time_range =last_time -first_time
        else :
            first_time =0
            time_range =180
        if time_range ==0 :
            time_range =180
        for action in replay .actions :
            timestamp =action .get ('timestamp',0 )
            x =int ((timestamp -first_time )/time_range *(width -40 ))+20
            cv2 .line (timeline ,(x ,20 ),(x ,height -20 ),self .colors ['ally'],2 )
        for i in range (0 ,int (time_range ),30 ):
            x =int (i /time_range *(width -40 ))+20
            minutes =i //60
            seconds =i %60
            cv2 .putText (
            timeline ,f"{minutes }:{seconds :02d}",
            (x -20 ,height -5 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.4 ,
            self .colors ['text'],1
            )
        return timeline
    def show_interactive (self ,replay ):
        frame_idx =0
        playing =False
        while True :
            frame_path =replay .get_frame_path (frame_idx )
            if os .path .exists (frame_path ):
                frame =cv2 .imread (frame_path )
                state =replay .get_state_at_frame (frame_idx )
                action =replay .get_action_at_frame (frame_idx )
                vis_frame =self .visualize_frame (frame ,state ,action )
                cv2 .putText (
                vis_frame ,f"Frame: {frame_idx }/{replay .total_frames }",
                (10 ,vis_frame .shape [0 ]-10 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.5 ,
                self .colors ['text'],1
                )
                cv2 .imshow ('Просмотр повторов',vis_frame )
            key =cv2 .waitKey (100 if playing else 0 )&0xFF
            if key ==ord ('q'):
                break
            elif key ==ord (' '):
                playing =not playing
            elif key ==ord ('d')or key ==83 :
                frame_idx =min (frame_idx +1 ,replay .total_frames -1 )
            elif key ==ord ('a')or key ==81 :
                frame_idx =max (frame_idx -1 ,0 )
            elif playing :
                frame_idx =min (frame_idx +1 ,replay .total_frames -1 )
        cv2 .destroyAllWindows ()