import os
import cv2
import numpy as np
class VideoExporter :
    def __init__ (self ,output_dir ="exports"):
        self .output_dir =output_dir
        os .makedirs (output_dir ,exist_ok =True )
    def export (self ,replay ,output_filename =None ,fps =10 ,add_overlay =True ):
        if output_filename is None :
            output_filename =f"replay_{replay .match_id }.mp4"
        output_path =os .path .join (self .output_dir ,output_filename )
        first_frame_path =replay .get_frame_path (0 )
        if not os .path .exists (first_frame_path ):
            raise FileNotFoundError ("Кадры реплея не найдены")
        first_frame =cv2 .imread (first_frame_path )
        height ,width =first_frame .shape [:2 ]
        fourcc =cv2 .VideoWriter_fourcc (*'mp4v')
        video =cv2 .VideoWriter (output_path ,fourcc ,fps ,(width ,height ))
        for frame_id in range (replay .total_frames ):
            frame_path =replay .get_frame_path (frame_id )
            if not os .path .exists (frame_path ):
                continue
            frame =cv2 .imread (frame_path )
            if add_overlay :
                state =replay .get_state_at_frame (frame_id )
                action =replay .get_action_at_frame (frame_id )
                frame =self ._add_overlay (frame ,frame_id ,replay ,state ,action )
            video .write (frame )
        video .release ()
        return output_path
    def _add_overlay (self ,frame ,frame_id ,replay ,state ,action ):
        overlay =frame .copy ()
        cv2 .rectangle (overlay ,(0 ,0 ),(frame .shape [1 ],100 ),(0 ,0 ,0 ),-1 )
        frame =cv2 .addWeighted (overlay ,0.7 ,frame ,0.3 ,0 )
        cv2 .putText (
        frame ,f"Frame: {frame_id }/{replay .total_frames }",
        (10 ,30 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.7 ,(255 ,255 ,255 ),2
        )
        if state :
            game_state =state .get ('state',{})
            elixir =game_state .get ('elixir_blue',0 )
            towers_blue =game_state .get ('towers_blue',3 )
            towers_red =game_state .get ('towers_red',3 )
            chrono =game_state .get ('chrono',0 )
            cv2 .putText (
            frame ,f"Elixir: {elixir }",
            (10 ,60 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.6 ,(255 ,105 ,180 ),2
            )
            cv2 .putText (
            frame ,f"Towers: {towers_blue }-{towers_red }",
            (150 ,60 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.6 ,(255 ,255 ,255 ),2
            )
            cv2 .putText (
            frame ,f"Time: {chrono //60 }:{chrono %60 :02d}",
            (300 ,60 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.6 ,(255 ,255 ,255 ),2
            )
        if action and action .get ('action'):
            cv2 .putText (
            frame ,"ДЕЙСТВИЕ!",
            (frame .shape [1 ]-120 ,30 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.8 ,
            (0 ,255 ,0 ),2
            )
        return frame
    def export_with_analysis (self ,replay ,analyzer ,output_filename =None ):
        if output_filename is None :
            output_filename =f"replay_{replay .match_id }_analyzed.mp4"
        output_path =os .path .join (self .output_dir ,output_filename )
        errors =analyzer .analyze_replay (replay )
        error_frames ={e .get ('frame_id'):e for e in errors if 'frame_id'in e }
        first_frame_path =replay .get_frame_path (0 )
        first_frame =cv2 .imread (first_frame_path )
        height ,width =first_frame .shape [:2 ]
        fourcc =cv2 .VideoWriter_fourcc (*'mp4v')
        video =cv2 .VideoWriter (output_path ,fourcc ,10 ,(width ,height ))
        for frame_id in range (replay .total_frames ):
            frame_path =replay .get_frame_path (frame_id )
            if not os .path .exists (frame_path ):
                continue
            frame =cv2 .imread (frame_path )
            state =replay .get_state_at_frame (frame_id )
            action =replay .get_action_at_frame (frame_id )
            frame =self ._add_overlay (frame ,frame_id ,replay ,state ,action )
            if frame_id in error_frames :
                error =error_frames [frame_id ]
                frame =self ._add_error_overlay (frame ,error )
            video .write (frame )
        video .release ()
        return output_path
    def _add_error_overlay (self ,frame ,error ):
        severity_colors ={
        'high':(0 ,0 ,255 ),
        'medium':(0 ,165 ,255 ),
        'low':(0 ,255 ,255 )
        }
        color =severity_colors .get (error .get ('severity','low'),(255 ,255 ,255 ))
        cv2 .rectangle (
        frame ,
        (5 ,frame .shape [0 ]-80 ),
        (frame .shape [1 ]-5 ,frame .shape [0 ]-5 ),
        color ,3
        )
        cv2 .putText (
        frame ,f"ERROR: {error .get ('description','Unknown')[:50 ]}",
        (15 ,frame .shape [0 ]-50 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.5 ,color ,2
        )
        cv2 .putText (
        frame ,f"TIP: {error .get ('recommendation','')[:50 ]}",
        (15 ,frame .shape [0 ]-20 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.5 ,(255 ,255 ,255 ),1
        )
        return frame
    def create_highlight_reel (self ,replays ,output_filename ="highlights.mp4"):
        output_path =os .path .join (self .output_dir ,output_filename )
        highlights =[]
        for replay in replays :
            for action in replay .actions :
                if action .get ('action'):
                    highlights .append ({
                    'replay':replay ,
                    'frame_id':action .get ('frame_id'),
                    'action':action
                    })
        if not highlights :
            return None
        first_frame =cv2 .imread (highlights [0 ]['replay'].get_frame_path (0 ))
        height ,width =first_frame .shape [:2 ]
        fourcc =cv2 .VideoWriter_fourcc (*'mp4v')
        video =cv2 .VideoWriter (output_path ,fourcc ,10 ,(width ,height ))
        for hl in highlights [:20 ]:
            replay =hl ['replay']
            center_frame =hl ['frame_id']
            for offset in range (-15 ,16 ):
                frame_id =center_frame +offset
                if frame_id <0 or frame_id >=replay .total_frames :
                    continue
                frame_path =replay .get_frame_path (frame_id )
                if os .path .exists (frame_path ):
                    frame =cv2 .imread (frame_path )
                    video .write (frame )
        video .release ()
        return output_path