import numpy as np
import time
try :
    import mss
    HAS_MSS =True
except ImportError :
    HAS_MSS =False
try :
    import dxcam
    HAS_DXCAM =True
except ImportError :
    HAS_DXCAM =False
try :
    import cv2
    HAS_CV2 =True
except ImportError :
    HAS_CV2 =False
class ScreenOptimizer :
    def __init__ (self ,method ='auto'):
        self .method =self ._select_method (method )
        self .capturer =None
        self .capture_region =None
        self .frame_times =[]
        self .last_frame =None
        self ._initialize_capturer ()
    def _select_method (self ,method ):
        if method =='auto':
            if HAS_DXCAM :
                return 'dxcam'
            elif HAS_MSS :
                return 'mss'
            else :
                return 'opencv'
        return method
    def _initialize_capturer (self ):
        if self .method =='dxcam'and HAS_DXCAM :
            self .capturer =dxcam .create ()
        elif self .method =='mss'and HAS_MSS :
            self .capturer =mss .mss ()
    def set_region (self ,x ,y ,width ,height ):
        self .capture_region ={
        'left':x ,
        'top':y ,
        'width':width ,
        'height':height
        }
    def auto_detect_window (self ,window_title ="BlueStacks"):
        try :
            import win32gui
            def callback (hwnd ,windows ):
                if win32gui .IsWindowVisible (hwnd ):
                    title =win32gui .GetWindowText (hwnd )
                    if window_title .lower ()in title .lower ():
                        rect =win32gui .GetWindowRect (hwnd )
                        windows .append (rect )
                return True
            windows =[]
            win32gui .EnumWindows (callback ,windows )
            if windows :
                left ,top ,right ,bottom =windows [0 ]
                self .set_region (left ,top ,right -left ,bottom -top )
                return True
        except Exception as e :
            print (f"Ошибка определения окна: {e }")
        return False
    def capture (self ):
        start_time =time .time ()
        frame =None
        if self .method =='dxcam'and self .capturer :
            frame =self ._capture_dxcam ()
        elif self .method =='mss'and self .capturer :
            frame =self ._capture_mss ()
        else :
            frame =self ._capture_opencv ()
        elapsed =time .time ()-start_time
        self .frame_times .append (elapsed )
        self .last_frame =frame
        return frame
    def _capture_dxcam (self ):
        if self .capture_region :
            region =(
            self .capture_region ['left'],
            self .capture_region ['top'],
            self .capture_region ['left']+self .capture_region ['width'],
            self .capture_region ['top']+self .capture_region ['height']
            )
            frame =self .capturer .grab (region =region )
        else :
            frame =self .capturer .grab ()
        if frame is not None :
            return cv2 .cvtColor (frame ,cv2 .COLOR_RGB2BGR )
        return None
    def _capture_mss (self ):
        if self .capture_region :
            monitor =self .capture_region
        else :
            monitor =self .capturer .monitors [1 ]
        screenshot =self .capturer .grab (monitor )
        frame =np .array (screenshot )
        return cv2 .cvtColor (frame ,cv2 .COLOR_BGRA2BGR )
    def _capture_opencv (self ):
        try :
            import pyautogui
            screenshot =pyautogui .screenshot (
            region =(
            self .capture_region ['left'],
            self .capture_region ['top'],
            self .capture_region ['width'],
            self .capture_region ['height']
            )if self .capture_region else None
            )
            return cv2 .cvtColor (np .array (screenshot ),cv2 .COLOR_RGB2BGR )
        except Exception :
            return None
    def start_continuous_capture (self ,target_fps =30 ):
        if self .method =='dxcam'and self .capturer :
            self .capturer .start (target_fps =target_fps )
    def stop_continuous_capture (self ):
        if self .method =='dxcam'and self .capturer :
            self .capturer .stop ()
    def get_latest_frame (self ):
        if self .method =='dxcam'and self .capturer :
            frame =self .capturer .get_latest_frame ()
            if frame is not None :
                return cv2 .cvtColor (frame ,cv2 .COLOR_RGB2BGR )
        return self .last_frame
    def get_fps (self ):
        if not self .frame_times :
            return 0
        recent =self .frame_times [-30 :]
        avg_time =sum (recent )/len (recent )
        return 1 /avg_time if avg_time >0 else 0
    def get_stats (self ):
        return {
        'method':self .method ,
        'fps':round (self .get_fps (),1 ),
        'captures':len (self .frame_times ),
        'region':self .capture_region ,
        'avg_capture_time':(
        sum (self .frame_times [-100 :])/len (self .frame_times [-100 :])*1000
        if self .frame_times else 0
        )
        }
    def benchmark (self ,num_frames =100 ):
        times =[]
        for _ in range (num_frames ):
            start =time .time ()
            self .capture ()
            times .append (time .time ()-start )
        return {
        'method':self .method ,
        'total_frames':num_frames ,
        'total_time':sum (times ),
        'avg_fps':num_frames /sum (times ),
        'min_time':min (times )*1000 ,
        'max_time':max (times )*1000 ,
        'avg_time':(sum (times )/num_frames )*1000
        }
    def cleanup (self ):
        if self .method =='dxcam'and self .capturer :
            try :
                self .capturer .stop ()
            except :
                pass