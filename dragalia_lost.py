import pyautogui
import inputs
from inputs import devices, get_gamepad

# Constants
SCREEN_W = 1920
SCREEN_H = 1080
CENTER_X = SCREEN_W / 2
CENTER_Y = SCREEN_H / 2
MOVE_DELTA = 175
DEAD_ZONE = 2000
FLICK_ZONE = 10000
JOY_MIN = 0
JOY_MAX = 30000
REFRESH_HZ = 60

# Global variables
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
game_buttons = {
    'attack' : {'x' : SCREEN_W / 2, 'y' : SCREEN_H / 2, 'button' : joystick_map['attack']},
    'skill_1' : {'x' : 875, 'y' : 900, 'button' : joystick_map['skill_1']},
    'skill_2' : {'x' : 1000, 'y' : 900, 'button' : joystick_map['skill_2']},
    'skill_3' : {'x' : 1100, 'y' : 900, 'button' : joystick_map['skill_3']},
    'dragon' : {'x' : 750, 'y' : 750, 'button' : joystick_map['dragon']},
    'helper' : {'x' : 1200, 'y' : 900, 'button' : joystick_map['helper']},
    'minimap' : {'x' : 1165, 'y' : 135, 'button' : joystick_map['minimap']},
    'unpause' : {'x' : 850, 'y' : 750, 'button' : joystick_map['pause']},
    'pause' : {'x' : 1215, 'y' : 90, 'button' : joystick_map['pause']},
    'char_1' : {'x' : 710, 'y' : 95, 'button' : joystick_map['char_ud']},
    'char_2' : {'x' : 710, 'y' : 150, 'button' : joystick_map['char_ud']},
    'char_3' : {'x' : 710, 'y' : 210, 'button' : joystick_map['char_ud']},
    'char_4' : {'x' : 710, 'y' : 275, 'button' : joystick_map['char_ud']}
}

# Centers mouse
def reset_mouse():
    pyautogui.moveTo(CENTER_X, CENTER_Y)

# MousesDown at coordinate if state != 0, otherwise mouseUp and reset
def click_mouse(x, y, state):
    if (state == 1 or state == -1):
        pyautogui.mouseDown(x, y)
    elif state == 0:
        pyautogui.mouseUp()
        reset_mouse()

# Presses button based on input event name
def press(joy_in, state):
    global paused
    if (inv_joystick[joy_in] == 'pause' and state == 1):
        button = 'pause' if paused else 'unpause'
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
        pyautogui.mouseDown(CENTER_X, CENTER_Y)
        ljoy_held = True
    pyautogui.moveTo(CENTER_X + move_x, CENTER_Y + move_y)

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
        pyautogui.mouseDown(CENTER_X, CENTER_Y)
        pyautogui.moveTo(CENTER_X + move_x, CENTER_Y + move_y)
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
    events = get_gamepad()
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
            elif event.code == joystick_map['pause']:
                press(event.code, event.state)
            else:
                try:
                    press(event.code, event.state)
                except KeyError:
                    print('Button', event.code, 'not yet supported!')

if __name__ == '__main__':
    print('Starting!')
    reset_mouse()
    try:
        joystick = inputs.devices.gamepads[0]
    except Exception:
        print('No joystick found!')
        exit()
    print('Using', joystick)
    pyautogui.PAUSE = 1 / REFRESH_HZ
    pyautogui.FAILSAFE = True
    print('Running...')
    while True:
        main_loop()
    