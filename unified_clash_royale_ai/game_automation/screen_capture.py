import cv2
import numpy as np
import mss
import os
import sys
try :
    import dxcam
except ImportError :
    dxcam =None
import pygetwindow as gw
sys .path .insert (0 ,os .path .dirname (os .path .dirname (os .path .abspath (__file__ ))))
from unified_clash_royale_ai .config import GAME_MON
class ScreenCapture :
    def __init__ (self ,window_title ='LDPlayer',use_dxcam =True ):
        self .window_title =window_title
        self .use_dxcam =use_dxcam
        self .app_window =None
        self .camera =None
        try :
            windows =gw .getWindowsWithTitle (window_title )
            if windows :
                self .app_window =windows [0 ]
                if self .app_window .isMinimized :
                    self .app_window .restore ()
                self .app_window .activate ()
        except Exception as e :
            print (f"Warning: Could not find window {window_title }: {e }")
        if use_dxcam and dxcam is not None :
            try :
                self .camera =dxcam .create (output_color ="BGR")
            except Exception as e :
                print (f"Warning: Could not initialize dxcam: {e }")
                self .use_dxcam =False
        else :
            self .use_dxcam =False
    def take_screenshot (self ,resize =True ,rectangle_corners =None ,full_screen =False ):
        if self .app_window is None :
            raise ValueError ("Окно не найдено. Пожалуйста, проверьте заголовок окна.")
        if full_screen :
            monitor =(0 ,0 ,self .app_window .width ,self .app_window .height )
        elif rectangle_corners :
            left =self .app_window .left +rectangle_corners [0 ][0 ]
            top =self .app_window .top +rectangle_corners [0 ][1 ]
            width =rectangle_corners [1 ][0 ]-rectangle_corners [0 ][0 ]
            height =rectangle_corners [1 ][1 ]-rectangle_corners [0 ][1 ]
            monitor =(left ,top ,left +width ,top +height )
        else :
            monitor ={
            "top":self .app_window .top ,
            "left":self .app_window .left ,
            "width":self .app_window .width ,
            "height":self .app_window .height
            }
        if self .use_dxcam and self .camera and not isinstance (monitor ,dict ):
            try :
                screenshot =self .camera .grab (region =monitor )
                if screenshot is not None :
                    screenshot =np .array (screenshot )
                    if screenshot .dtype !="object":
                        if resize :
                            screenshot =cv2 .resize (screenshot ,(0 ,0 ),fx =1.0 ,fy =1.0 )
                        return screenshot
            except Exception as e :
                print (f"dxcam failed, using mss: {e }")
        with mss .mss ()as sct :
            if isinstance (monitor ,dict ):
                screenshot =np .array (sct .grab (monitor ))[:,:,:3 ]
            else :
                monitor_dict ={
                "top":monitor [1 ],
                "left":monitor [0 ],
                "width":monitor [2 ]-monitor [0 ],
                "height":monitor [3 ]-monitor [1 ]
                }
                screenshot =np .array (sct .grab (monitor_dict ))[:,:,:3 ]
        if resize :
            screenshot =cv2 .resize (screenshot ,(0 ,0 ),fx =1.0 ,fy =1.0 )
        return screenshot
    def process_image (self ,image ,target_size =(208 ,160 ),grayscale =True ):
        if grayscale :
            image =cv2 .cvtColor (image ,cv2 .COLOR_BGR2GRAY )
        image =cv2 .resize (image ,target_size )
        image =image .astype (np .float32 )/255.0
        if grayscale :
            image =np .expand_dims (image ,axis =-1 )
        return image
    def get_window_coords (self ):
        if self .app_window :
            return (self .app_window .left ,self .app_window .top )
        return (0 ,0 )
    def get_window_size (self ):
        if self .app_window :
            return (self .app_window .width ,self .app_window .height )
        return (0 ,0 )