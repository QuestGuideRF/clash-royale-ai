import tkinter as tk
from tkinter import ttk ,messagebox ,filedialog
from typing import Dict ,Optional ,Callable
class SettingsGUI :
    def __init__ (self ,settings_manager ,profile_manager =None ,
    calibrator =None ,on_save =None ):
        self .settings_manager =settings_manager
        self .profile_manager =profile_manager
        self .calibrator =calibrator
        self .on_save =on_save
        self .window =None
        self .widgets ={}
    def show (self ):
        if self .window is not None :
            self .window .lift ()
            return
        self .window =tk .Toplevel ()
        self .window .title ("Настройки")
        self .window .geometry ("600x500")
        self .window .protocol ("WM_DELETE_WINDOW",self ._on_close )
        self ._create_widgets ()
    def _create_widgets (self ):
        notebook =ttk .Notebook (self .window )
        notebook .pack (fill =tk .BOTH ,expand =True ,padx =5 ,pady =5 )
        self ._create_general_tab (notebook )
        self ._create_capture_tab (notebook )
        self ._create_recognition_tab (notebook )
        self ._create_bot_tab (notebook )
        self ._create_performance_tab (notebook )
        self ._create_hotkeys_tab (notebook )
        if self .profile_manager :
            self ._create_profiles_tab (notebook )
        if self .calibrator :
            self ._create_calibration_tab (notebook )
        button_frame =ttk .Frame (self .window )
        button_frame .pack (fill =tk .X ,padx =5 ,pady =5 )
        ttk .Button (button_frame ,text ="Сохранить",
        command =self ._save_settings ).pack (side =tk .RIGHT ,padx =5 )
        ttk .Button (button_frame ,text ="Отмена",
        command =self ._on_close ).pack (side =tk .RIGHT )
        ttk .Button (button_frame ,text ="Сбросить",
        command =self ._reset_settings ).pack (side =tk .LEFT )
    def _create_general_tab (self ,notebook ):
        frame =ttk .Frame (notebook ,padding =10 )
        notebook .add (frame ,text ="Общие")
        row =0
        ttk .Label (frame ,text ="Язык:").grid (row =row ,column =0 ,sticky ='w',pady =5 )
        lang_var =tk .StringVar (value =self .settings_manager .get ('general.language','ru'))
        lang_combo =ttk .Combobox (frame ,textvariable =lang_var ,values =['ru','en'])
        lang_combo .grid (row =row ,column =1 ,sticky ='w',pady =5 )
        self .widgets ['general.language']=lang_var
        row +=1
        ttk .Label (frame ,text ="Тема:").grid (row =row ,column =0 ,sticky ='w',pady =5 )
        theme_var =tk .StringVar (value =self .settings_manager .get ('general.theme','dark'))
        theme_combo =ttk .Combobox (frame ,textvariable =theme_var ,values =['dark','light'])
        theme_combo .grid (row =row ,column =1 ,sticky ='w',pady =5 )
        self .widgets ['general.theme']=theme_var
        row +=1
        auto_start_var =tk .BooleanVar (value =self .settings_manager .get ('general.auto_start',False ))
        ttk .Checkbutton (frame ,text ="Автозапуск при старте Windows",
        variable =auto_start_var ).grid (row =row ,column =0 ,columnspan =2 ,sticky ='w',pady =5 )
        self .widgets ['general.auto_start']=auto_start_var
        row +=1
        minimize_var =tk .BooleanVar (value =self .settings_manager .get ('general.minimize_to_tray',True ))
        ttk .Checkbutton (frame ,text ="Сворачивать в трей",
        variable =minimize_var ).grid (row =row ,column =0 ,columnspan =2 ,sticky ='w',pady =5 )
        self .widgets ['general.minimize_to_tray']=minimize_var
    def _create_capture_tab (self ,notebook ):
        frame =ttk .Frame (notebook ,padding =10 )
        notebook .add (frame ,text ="Захват экрана")
        row =0
        ttk .Label (frame ,text ="Метод захвата:").grid (row =row ,column =0 ,sticky ='w',pady =5 )
        method_var =tk .StringVar (value =self .settings_manager .get ('screen_capture.method','auto'))
        method_combo =ttk .Combobox (frame ,textvariable =method_var ,
        values =['auto','mss','dxcam'])
        method_combo .grid (row =row ,column =1 ,sticky ='w',pady =5 )
        self .widgets ['screen_capture.method']=method_var
        row +=1
        ttk .Label (frame ,text ="Целевой FPS:").grid (row =row ,column =0 ,sticky ='w',pady =5 )
        fps_var =tk .IntVar (value =self .settings_manager .get ('screen_capture.target_fps',30 ))
        fps_spin =ttk .Spinbox (frame ,from_ =1 ,to =120 ,textvariable =fps_var ,width =10 )
        fps_spin .grid (row =row ,column =1 ,sticky ='w',pady =5 )
        self .widgets ['screen_capture.target_fps']=fps_var
        row +=1
        ttk .Label (frame ,text ="Название окна:").grid (row =row ,column =0 ,sticky ='w',pady =5 )
        window_var =tk .StringVar (value =self .settings_manager .get ('screen_capture.window_title','BlueStacks'))
        window_entry =ttk .Entry (frame ,textvariable =window_var ,width =30 )
        window_entry .grid (row =row ,column =1 ,sticky ='w',pady =5 )
        self .widgets ['screen_capture.window_title']=window_var
    def _create_recognition_tab (self ,notebook ):
        frame =ttk .Frame (notebook ,padding =10 )
        notebook .add (frame ,text ="Распознавание")
        row =0
        ttk .Label (frame ,text ="Порог уверенности:").grid (row =row ,column =0 ,sticky ='w',pady =5 )
        conf_var =tk .DoubleVar (value =self .settings_manager .get ('recognition.confidence_threshold',0.7 ))
        conf_scale =ttk .Scale (frame ,from_ =0.1 ,to =1.0 ,variable =conf_var ,orient =tk .HORIZONTAL )
        conf_scale .grid (row =row ,column =1 ,sticky ='ew',pady =5 )
        ttk .Label (frame ,textvariable =conf_var ).grid (row =row ,column =2 ,pady =5 )
        self .widgets ['recognition.confidence_threshold']=conf_var
        row +=1
        gpu_var =tk .BooleanVar (value =self .settings_manager .get ('recognition.use_gpu',True ))
        ttk .Checkbutton (frame ,text ="Использовать GPU",
        variable =gpu_var ).grid (row =row ,column =0 ,columnspan =2 ,sticky ='w',pady =5 )
        self .widgets ['recognition.use_gpu']=gpu_var
    def _create_bot_tab (self ,notebook ):
        frame =ttk .Frame (notebook ,padding =10 )
        notebook .add (frame ,text ="Бот")
        row =0
        ttk .Label (frame ,text ="Режим:").grid (row =row ,column =0 ,sticky ='w',pady =5 )
        mode_var =tk .StringVar (value =self .settings_manager .get ('bot.mode','balanced'))
        mode_combo =ttk .Combobox (frame ,textvariable =mode_var ,
        values =['fast','balanced','accurate'])
        mode_combo .grid (row =row ,column =1 ,sticky ='w',pady =5 )
        self .widgets ['bot.mode']=mode_var
        row +=1
        ttk .Label (frame ,text ="Задержка реакции (сек):").grid (row =row ,column =0 ,sticky ='w',pady =5 )
        delay_var =tk .DoubleVar (value =self .settings_manager .get ('bot.reaction_delay',0.1 ))
        delay_spin =ttk .Spinbox (frame ,from_ =0.0 ,to =1.0 ,increment =0.05 ,
        textvariable =delay_var ,width =10 )
        delay_spin .grid (row =row ,column =1 ,sticky ='w',pady =5 )
        self .widgets ['bot.reaction_delay']=delay_var
        row +=1
        auto_var =tk .BooleanVar (value =self .settings_manager .get ('bot.auto_play',False ))
        ttk .Checkbutton (frame ,text ="Автоматическая игра",
        variable =auto_var ).grid (row =row ,column =0 ,columnspan =2 ,sticky ='w',pady =5 )
        self .widgets ['bot.auto_play']=auto_var
    def _create_performance_tab (self ,notebook ):
        frame =ttk .Frame (notebook ,padding =10 )
        notebook .add (frame ,text ="Производительность")
        row =0
        cache_var =tk .BooleanVar (value =self .settings_manager .get ('performance.cache_enabled',True ))
        ttk .Checkbutton (frame ,text ="Включить кэширование",
        variable =cache_var ).grid (row =row ,column =0 ,columnspan =2 ,sticky ='w',pady =5 )
        self .widgets ['performance.cache_enabled']=cache_var
        row +=1
        parallel_var =tk .BooleanVar (value =self .settings_manager .get ('performance.parallel_processing',True ))
        ttk .Checkbutton (frame ,text ="Параллельная обработка",
        variable =parallel_var ).grid (row =row ,column =0 ,columnspan =2 ,sticky ='w',pady =5 )
        self .widgets ['performance.parallel_processing']=parallel_var
        row +=1
        ttk .Label (frame ,text ="Количество воркеров:").grid (row =row ,column =0 ,sticky ='w',pady =5 )
        workers_var =tk .IntVar (value =self .settings_manager .get ('performance.num_workers',4 ))
        workers_spin =ttk .Spinbox (frame ,from_ =1 ,to =16 ,textvariable =workers_var ,width =10 )
        workers_spin .grid (row =row ,column =1 ,sticky ='w',pady =5 )
        self .widgets ['performance.num_workers']=workers_var
    def _create_hotkeys_tab (self ,notebook ):
        frame =ttk .Frame (notebook ,padding =10 )
        notebook .add (frame ,text ="Горячие клавиши")
        hotkeys ={
        'start_stop':'Старт/Стоп',
        'pause':'Пауза',
        'screenshot':'Скриншот',
        'settings':'Настройки'
        }
        for row ,(key ,label )in enumerate (hotkeys .items ()):
            ttk .Label (frame ,text =f"{label }:").grid (row =row ,column =0 ,sticky ='w',pady =5 )
            var =tk .StringVar (value =self .settings_manager .get (f'hotkeys.{key }',''))
            entry =ttk .Entry (frame ,textvariable =var ,width =15 )
            entry .grid (row =row ,column =1 ,sticky ='w',pady =5 )
            self .widgets [f'hotkeys.{key }']=var
    def _create_profiles_tab (self ,notebook ):
        frame =ttk .Frame (notebook ,padding =10 )
        notebook .add (frame ,text ="Профили")
        profiles_list =tk .Listbox (frame ,height =8 )
        profiles_list .pack (fill =tk .BOTH ,expand =True ,pady =5 )
        for profile in self .profile_manager .list_profiles ():
            prefix ="✓ "if profile ['active']else "  "
            profiles_list .insert (tk .END ,f"{prefix }{profile ['name']}")
        btn_frame =ttk .Frame (frame )
        btn_frame .pack (fill =tk .X ,pady =5 )
        ttk .Button (btn_frame ,text ="Применить",
        command =lambda :self ._apply_profile (profiles_list )).pack (side =tk .LEFT ,padx =2 )
        ttk .Button (btn_frame ,text ="Создать",
        command =self ._create_profile ).pack (side =tk .LEFT ,padx =2 )
        ttk .Button (btn_frame ,text ="Удалить",
        command =lambda :self ._delete_profile (profiles_list )).pack (side =tk .LEFT ,padx =2 )
    def _create_calibration_tab (self ,notebook ):
        frame =ttk .Frame (notebook ,padding =10 )
        notebook .add (frame ,text ="Калибровка")
        status =self .calibrator .get_calibration_status ()
        ttk .Label (frame ,text =f"Размер экрана: {status ['screen_size']}").pack (anchor ='w',pady =2 )
        ttk .Label (frame ,text =f"Масштаб: {status ['scale']}").pack (anchor ='w',pady =2 )
        ttk .Label (frame ,text =f"Смещение: {status ['offset']}").pack (anchor ='w',pady =2 )
        ttk .Separator (frame ,orient ='horizontal').pack (fill ='x',pady =10 )
        ttk .Button (frame ,text ="Автоопределение",
        command =self ._auto_calibrate ).pack (pady =5 )
        ttk .Button (frame ,text ="Ручная калибровка",
        command =self ._manual_calibrate ).pack (pady =5 )
        ttk .Button (frame ,text ="Тест калибровки",
        command =self ._test_calibration ).pack (pady =5 )
    def _save_settings (self ):
        for path ,widget in self .widgets .items ():
            value =widget .get ()
            self .settings_manager .set (path ,value )
        if self .on_save :
            self .on_save ()
        messagebox .showinfo ("Успех","Настройки сохранены")
    def _reset_settings (self ):
        if messagebox .askyesno ("Подтверждение","Сбросить все настройки?"):
            self .settings_manager .reset ()
            self ._on_close ()
            self .show ()
    def _on_close (self ):
        if self .window :
            self .window .destroy ()
            self .window =None
    def _apply_profile (self ,listbox ):
        selection =listbox .curselection ()
        if selection :
            profiles =self .profile_manager .list_profiles ()
            profile_id =profiles [selection [0 ]]['id']
            self .profile_manager .apply_profile (profile_id ,self .settings_manager )
            messagebox .showinfo ("Успех",f"Профиль применен")
    def _create_profile (self ):
        dialog =tk .Toplevel (self .window )
        dialog .title ("Новый профиль")
        dialog .geometry ("300x150")
        ttk .Label (dialog ,text ="Название:").pack (pady =5 )
        name_var =tk .StringVar ()
        ttk .Entry (dialog ,textvariable =name_var ).pack (pady =5 )
        def save ():
            name =name_var .get ()
            if name :
                profile_id =name .lower ().replace (' ','_')
                self .profile_manager .create_from_current (
                self .settings_manager ,profile_id ,name ,"Пользовательский профиль"
                )
                dialog .destroy ()
        ttk .Button (dialog ,text ="Создать",command =save ).pack (pady =10 )
    def _delete_profile (self ,listbox ):
        selection =listbox .curselection ()
        if selection :
            profiles =self .profile_manager .list_profiles ()
            profile =profiles [selection [0 ]]
            if profile ['custom']:
                if messagebox .askyesno ("Подтверждение",f"Удалить профиль {profile ['name']}?"):
                    self .profile_manager .delete_profile (profile ['id'])
                    listbox .delete (selection [0 ])
            else :
                messagebox .showwarning ("Ошибка","Нельзя удалить встроенный профиль")
    def _auto_calibrate (self ):
        messagebox .showinfo ("Калибровка","Сделайте скриншот игры для калибровки")
    def _manual_calibrate (self ):
        messagebox .showinfo ("Калибровка","Ручная калибровка пока не реализована")
    def _test_calibration (self ):
        messagebox .showinfo ("Калибровка","Тест калибровки пока не реализован")