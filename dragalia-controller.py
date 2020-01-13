import inputs
import pyautogui
from win32gui import GetForegroundWindow, FindWindow, GetWindowRect
from inputs import devices, get_gamepad

# CHANGE ME
WINDOW_TITLE = 'Pixel 2'
UI_LAYOUT = 'right'
TITLE_OFFSET = 30

# Constants
MOVE_DELTA = 175
DEAD_ZONE = 2000
FLICK_ZONE = 10000
JOY_MIN = 0
JOY_MAX = 30000
REFRESH_HZ = 120

# Global variables
left_x = 0
left_y = 0
right_x = 0
right_y = 0
screen_w = 1920
screen_h = 1080
wincenter_x = 0
wincenter_y = 0
current_char = 1
x_set = False
y_set = False
move_x = 0
move_y = 0
ljoy_held = False
l_seen_x = False
l_seen_y = False
slx_val = 0
sly_val = 0
rjoy_held = False
r_seen_x = False
r_seen_y = False
srx_val = 0
sry_val = 0
paused = False

# Maps controller to inputs
xbox_map = {
    'A' : 'BTN_SOUTH',
    'B' : 'BTN_EAST',
    'X' : 'BTN_WEST',
    'Y' : 'BTN_NORTH',
    'LB' : 'BTN_TL',
    'RB' : 'BTN_TR',
    'START' : 'BTN_SELECT',
    'SHARE' : 'BTN_START',
    'DP_UD' : 'ABS_HAT0Y',
    'DP_LR' : 'ABS_HAT0X',
    'LJOY_X' : 'ABS_X',
    'LJOY_Y' : 'ABS_Y',
    'RJOY_X' : 'ABS_RX',
    'RJOY_Y' : 'ABS_RY'
}

# Maps actions to inputs
joystick_map = {
    'attack' : xbox_map['A'],
    'skill_1' : xbox_map['X'],
    'skill_2' : xbox_map['Y'],
    'skill_3' : xbox_map['B'],
    'dragon' : xbox_map['LB'],
    'helper' : xbox_map['RB'],
    'pause' : xbox_map['START'],
    'minimap' : xbox_map['SHARE'],
    'char_ud' : xbox_map['DP_UD'],
    'move_x' : xbox_map['LJOY_X'],
    'move_y' : xbox_map['LJOY_Y'],
    'dodge_x' : xbox_map['RJOY_X'],
    'dodge_y' : xbox_map['RJOY_Y']
    #'char_up' : xbox_map['DP_UD'],
    #'char_down' : xbox_map['DP_UD']
    #'char_1' : xbox_map[''],
    #'char_2' : xbox_map['']
    #'char_3' : xbox_map[''],
    #'char_4' : xbox_map['']
}

# Maps inputs to actions
inv_joystick = { v: k for k, v in joystick_map.items()}

# Maps actions to coordinates and joystick buttons
# x and y are calculated based on window position
# delta_x and delta_y are fractional offsets from default UI layout right corner for ratio scaling
# skill_2 and skill_3 will be offsets from skill_1 depending on corner
game_buttons = {
    'attack' : {'x' : wincenter_x, 'y' : wincenter_y, 'delta_x' : 0, 'delta_y' : 0, 'button' : joystick_map['attack']},
    'skill_1' : {'x' : 875, 'y' : 900, 'delta_x' : 0.3500, 'delta_y' : 0.0682, 'button' : joystick_map['skill_1']},
    'skill_2' : {'x' : 1000, 'y' : 900, 'delta_x' : 0.1960, 'delta_y' : 0.93457, 'button' : joystick_map['skill_2']},
    'skill_3' : {'x' : 1100, 'y' : 900, 'delta_x' : 0.3920, 'delta_y' : 0.93457, 'button' : joystick_map['skill_3']},
    'dragon' : {'x' : 750, 'y' : 750, 'delta_x' : 0.1428, 'delta_y' : 0.2280, 'button' : joystick_map['dragon']},
    'helper' : {'x' : 1200, 'y' : 900, 'delta_x' : 0.0827, 'delta_y' : 0.0800, 'button' : joystick_map['helper']},
    'minimap' : {'x' : 1165, 'y' : 135, 'delta_x' : 0.1561, 'delta_y' : 0.0813, 'button' : joystick_map['minimap']},
    'unpause' : {'x' : 850, 'y' : 750, 'delta_x' : 0.4604, 'delta_y' : 0.5578, 'button' : joystick_map['pause']},
    'pause' : {'x' : 1215, 'y' : 90, 'delta_x' : 0.0660, 'delta_y' : 0.0373, 'button' : joystick_map['pause']},
    'char_1' : {'x' : 710, 'y' : 95, 'delta_x' : 0.0660, 'delta_y' : 0.0373, 'button' : joystick_map['char_ud']},
    'char_2' : {'x' : 710, 'y' : 150, 'delta_x' : 0.0660, 'delta_y' : 0.1018, 'button' : joystick_map['char_ud']},
    'char_3' : {'x' : 710, 'y' : 210, 'delta_x' : 0.0660, 'delta_y' : 0.1663, 'button' : joystick_map['char_ud']},
    'char_4' : {'x' : 710, 'y' : 275, 'delta_x' : 0.0660, 'delta_y' : 0.2317, 'button' : joystick_map['char_ud']}
}

# grabs coordinates for window with WINDOW_TITLE and updates wincenter_x and wincenter_y
def find_window():
    global wincenter_x, wincenter_y, screen_w, screen_h, left_x, left_y, right_x, right_y
    scr_win = FindWindow(None, WINDOW_TITLE)
    (left_x, left_y, right_x, right_y) = GetWindowRect(scr_win)
    screen_w = right_x - left_x
    screen_h = right_y - left_y - TITLE_OFFSET
    wincenter_x = int(left_x + (screen_w/2))
    wincenter_y = int(left_y + (screen_h/2))
    left_y = left_y + TITLE_OFFSET
    #print (screen_w, screen_h, wincenter_x, wincenter_y)
    compute_all()

# Helper to compute specific button based on delta_x, delta_y ratio for screen scaling
# Calculation changes based on UI Layout
def compute_button(name, corner):
    global game_buttons
    if corner == 'tl':
        new_x = left_x + (game_buttons[name]['delta_x'] * screen_w)
        new_y = left_y + (game_buttons[name]['delta_y'] * screen_h)
    elif corner == 'tr':
        new_x = right_x - (game_buttons[name]['delta_x'] * screen_w)
        new_y = left_y + (game_buttons[name]['delta_y'] * screen_h)
    elif corner == 'bl':
        if name == 'skill_2' or name == 'skill_3':
            new_x = game_buttons['skill_1']['x'] + (game_buttons[name]['delta_x'] * screen_w)
            new_y = game_buttons['skill_1']['y']
        else:
            new_x = left_x + (game_buttons[name]['delta_x'] * screen_w)
            new_y = right_y - (game_buttons[name]['delta_y'] * screen_h)
    elif corner == 'br':
        if name == 'skill_2' or name == 'skill_3':
            new_x = game_buttons['skill_1']['x'] - (game_buttons[name]['delta_x'] * screen_w)
            new_y = game_buttons['skill_1']['y']
        else:
            new_x = right_x - (game_buttons[name]['delta_x'] * screen_w)
            new_y = right_y - (game_buttons[name]['delta_y'] * screen_h)
    elif corner == 'center':
        new_x = wincenter_x - (game_buttons[name]['delta_x']/2 * screen_w)
        new_y = wincenter_y +    (game_buttons[name]['delta_y']/2 * screen_h)
    game_buttons[name]['x'] = int(new_x)
    game_buttons[name]['y'] = int(new_y)

# Calculates button positions based on center position
def compute_all():
    compute_button('attack', 'center')
    if UI_LAYOUT == 'right':
        compute_button('skill_1', 'bl')
        compute_button('skill_2', 'bl')
        compute_button('skill_3', 'bl')
        compute_button('dragon', 'bl')
        compute_button('helper', 'br')
    elif UI_LAYOUT == 'left':
        compute_button('skill_1', 'br')
        compute_button('skill_2', 'br')
        compute_button('skill_3', 'br')
        compute_button('dragon', 'br')
        compute_button('helper', 'bl')
    compute_button('minimap', 'tr')
    compute_button('unpause', 'center')
    compute_button('pause', 'tr')
    compute_button('char_1', 'tl')
    compute_button('char_2', 'tl')
    compute_button('char_3', 'tl')
    compute_button('char_4', 'tl')
    #print (game_buttons)

# Centers mouse
def reset_mouse():
    pyautogui.moveTo(wincenter_x, wincenter_y)

# MousesDown at coordinate if state != 0, otherwise mouseUp and reset
def click_mouse(x, y, state):
    if (state == 1 or state == -1):
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
    elif state == 0:
        pyautogui.mouseUp()
        reset_mouse()

# Presses button based on input event name
def press(joy_in, state):
    global paused
    if (inv_joystick[joy_in] == 'pause' and state == 1):
        button = 'unpause' if paused else 'pause'
        paused = not paused
    else:
        button = inv_joystick[joy_in]
    click_mouse(game_buttons[button]['x'], game_buttons[button]['y'], state)

# Presses button based on action name
def press2(char, state):
    click_mouse(game_buttons[char]['x'], game_buttons[char]['y'], state)

# Clicks and drags from center to x,y - will stay dragged if not reset
def click_drag_mouse(x, y):
    global x_set
    global y_set
    global move_x
    global move_y
    global ljoy_held
    move_x = scale(x)
    move_y = scale(-y)
    if not ljoy_held:
        reset_mouse()
        pyautogui.mouseUp()
        pyautogui.moveTo(wincenter_x, wincenter_y)
        pyautogui.mouseDown()
        ljoy_held = True
    pyautogui.moveTo(wincenter_x + move_x, wincenter_y + move_y)

    x_set = False
    y_set = False
    move_x = 0
    move_y = 0

# Quickly swipes from center to x,y and resets
def swipe(x, y):
    global move_x
    global move_y
    global rjoy_held
    move_x = scale(x)
    move_y = scale(-y)
    if not rjoy_held:
        reset_mouse()
        pyautogui.mouseUp()
        pyautogui.moveTo(wincenter_x, wincenter_y)
        pyautogui.mouseDown()
        pyautogui.moveTo(wincenter_x + move_x, wincenter_y + move_y)
        pyautogui.mouseUp()
        reset_mouse()
        rjoy_held = True
        move_x = 0
        move_y = 0

# Maps joystick values to the delta for linear movement
def scale(val):
    in_min = JOY_MIN if val > 0 else -JOY_MIN
    in_max = JOY_MAX if val > 0 else -JOY_MAX
    out_min = 0
    out_max = MOVE_DELTA if val > DEAD_ZONE else -MOVE_DELTA
    return out_min + (val - in_min) * ((out_max - out_min) / (in_max - in_min))

# Moves character selection up or down by one
def switch_char(direction, state):
    global current_char
    if direction == 'u':
        if current_char == 1:
            current_char = 4
        else:
            current_char -= 1
    elif direction == 'd':
        if current_char == 4:
            current_char = 1
        else:
            current_char += 1
    elif direction == 'z':
        pyautogui.mouseUp()
        reset_mouse()
        return
    switch_current_char = {
        1: lambda: press2('char_1', state),
        2: lambda: press2('char_2', state),
        3: lambda: press2('char_3', state),
        4: lambda: press2('char_4', state)
    }
    switch_current_char.get(current_char)()

# Continuous loop to check gamepad inputs
def main_loop():
    global ljoy_held
    global l_seen_x
    global l_seen_y
    global r_seen_x
    global r_seen_y
    global rjoy_held
    global slx_val
    global sly_val
    global srx_val
    global sry_val
    try:
        events = get_gamepad()
        find_window()
    except Exception as e:
        print('Exception', str(e))

    for event in events:
        if event.ev_type != 'Sync':
            #print(event.ev_type, event.code, event.state)
            if (event.code == joystick_map['move_x'] or event.code == joystick_map['move_y']):
                if event.code == joystick_map['move_x']:
                    l_seen_x = True
                    slx_val = event.state
                elif event.code == joystick_map['move_y']:
                    l_seen_y = True
                    sly_val = event.state
                if (l_seen_x and l_seen_y):
                    if (event.state < -DEAD_ZONE or event.state > DEAD_ZONE):
                        l_seen_x = False
                        l_seen_y = False
                        click_drag_mouse(slx_val, sly_val)
                    else:
                        ljoy_held = False
                        pyautogui.mouseUp()
            elif (event.code == joystick_map['dodge_x'] or event.code == joystick_map['dodge_y']):
                if event.code == joystick_map['dodge_x']:
                    r_seen_x = True
                    srx_val = event.state
                elif event.code == joystick_map['dodge_y']:
                    r_seen_y = True
                    sry_val = event.state
                if (r_seen_x and r_seen_y):
                    if (event.state < -FLICK_ZONE or event.state > FLICK_ZONE):
                        r_seen_x = False
                        r_seen_y = False
                        swipe(srx_val, sry_val)
                    else:
                        rjoy_held = False
                        pyautogui.mouseUp()
            elif event.code == joystick_map['char_ud']:
                if event.state == -1:
                    switch_char('u', event.state)
                elif event.state == 1:
                    switch_char('d', event.state)
                else:
                    switch_char('z', event.state)
            else:
                try:
                    press(event.code, event.state)
                except KeyError:
                    print('Button', event.code, 'not yet supported!')

if __name__ == '__main__':
    print('Starting!')
    
    try:
        joystick = inputs.devices.gamepads[0]
    except Exception:
        print('No joystick found!')
        exit()
    print('Using', joystick)
    pyautogui.PAUSE = 1 / REFRESH_HZ
    pyautogui.FAILSAFE = True
    print('Running...')
    find_window()
    reset_mouse()
    while True:
        main_loop()
    