import time
import pyautogui
from ..config import CARD_SLOTS_POSITIONS
class ActionExecutor :
    def __init__ (self ,window_coords =(0 ,0 )):
        self .window_coords =window_coords
        pyautogui .PAUSE =0.01
    def place_card (self ,card_slot_index ,position ):
        card_x =self .window_coords [0 ]+CARD_SLOTS_POSITIONS [card_slot_index ][0 ]
        card_y =self .window_coords [1 ]+CARD_SLOTS_POSITIONS [card_slot_index ][1 ]
        pyautogui .click (card_x ,card_y )
        time .sleep (0.01 )
        place_x =self .window_coords [0 ]+position [0 ]
        place_y =self .window_coords [1 ]+position [1 ]
        pyautogui .click (place_x ,place_y )
    def click (self ,position ):
        x =self .window_coords [0 ]+position [0 ]
        y =self .window_coords [1 ]+position [1 ]
        pyautogui .click (x ,y )
    def start_battle (self ):
        pass
    def exit_battle (self ):
        pass