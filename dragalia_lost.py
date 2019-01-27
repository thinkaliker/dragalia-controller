import pyautogui
import inputs
from inputs import devices, get_gamepad

screen_w = 1920
screen_h = 1080
center_x = screen_w / 2
center_y = screen_h / 2
move_delta = 175
current_char = 1
dead_zone = 1000
joy_min = 0
joy_max = 30000
refresh_hz = 100
x_set = False
y_set = False
move_x = 0
move_y = 0
joy_held = False
seen_x = False
seen_y = False
sx_val = 0
sy_val = 0

xbox_map = {
    'A' : 'BTN_SOUTH',
    'B' : 'BTN_EAST',
    'X' : 'BTN_WEST',
    'Y' : 'BTN_NORTH',
    'LB' : 'BTN_TL',
    'RB' : 'BTN_TR',
    'START' : 'BTN_START',
    'SHARE' : 'BTN_SELECT',
    'DP_UD' : 'ABS_HAT0Y',
    'DP_LR' : 'ABS_HAT0X',
    'LJOY_X' : 'ABS_X',
    'LJOY_Y' : 'ABS_Y'
}

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
    'move_y' : xbox_map['LJOY_Y']
    #'char_up' : xbox_map['DP_UD'],
    #'char_down' : xbox_map['DP_UD']
    #'char_1' : xbox_map[''],
    #'char_2' : xbox_map['']
    #'char_3' : xbox_map[''],
    #'char_4' : xbox_map['']
}

inv_joystick = { v: k for k, v in joystick_map.items()}

game_buttons = {
    'attack' : {'x' : screen_w / 2, 'y' : screen_h / 2, 'button' : joystick_map['attack']},
    'skill_1' : {'x' : 875, 'y' : 900, 'button' : joystick_map['skill_1']},
    'skill_2' : {'x' : 1000, 'y' : 900, 'button' : joystick_map['skill_2']},
    'skill_3' : {'x' : 1100, 'y' : 900, 'button' : joystick_map['skill_3']},
    'dragon' : {'x' : 750, 'y' : 750, 'button' : joystick_map['dragon']},
    'helper' : {'x' : 1200, 'y' : 900, 'button' : joystick_map['helper']},
    'pause' : {'x' : 1165, 'y' : 135, 'button' : joystick_map['pause']},
    'minimap' : {'x' : 1215, 'y' : 90, 'button' : joystick_map['minimap']},
    'char_1' : {'x' : 710, 'y' : 95, 'button' : joystick_map['char_ud']},
    'char_2' : {'x' : 710, 'y' : 150, 'button' : joystick_map['char_ud']},
    'char_3' : {'x' : 710, 'y' : 210, 'button' : joystick_map['char_ud']},
    'char_4' : {'x' : 710, 'y' : 275, 'button' : joystick_map['char_ud']}
}

def reset_mouse():
    pyautogui.moveTo(center_x, center_y)

def click_mouse(x, y, state):
    if (state == 1 or state == -1):
        pyautogui.mouseDown(x, y)
    elif (state == 0):
        pyautogui.mouseUp()
        reset_mouse()

def press(joy_in, state):
    button = inv_joystick[joy_in]
    click_mouse(game_buttons[button]['x'], game_buttons[button]['y'], state)

def press2(char, state):
    click_mouse(game_buttons[char]['x'], game_buttons[char]['y'], state)

def click_drag_mouse(x, y):
    global x_set
    global y_set
    global move_x
    global move_y
    global joy_held
    move_x = scale(x)
    move_y = scale(-y)
    if not joy_held:
        reset_mouse()
        pyautogui.mouseDown(center_x, center_y)
        joy_held = True
    pyautogui.moveTo(center_x + move_x, center_y + move_y)

    x_set = False
    y_set = False
    move_x = 0
    move_y = 0

def scale(val):
    in_min = joy_min if val > 0 else -joy_min
    in_max = joy_max if val > 0 else -joy_max
    out_min = 0
    out_max = move_delta if val > dead_zone else -move_delta
    return out_min + (val - in_min) * ((out_max - out_min) / (in_max - in_min))

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
    f = switch_current_char.get(current_char)
    f()

def update(joystick):
    events = get_gamepad()
    global joy_held
    global seen_x
    global seen_y
    global sx_val
    global sy_val
    for event in events:
        if event.ev_type != 'Sync':
            #print(event.ev_type, event.code, event.state)
            if (event.code == joystick_map['move_x'] or event.code == joystick_map['move_y']):
                if (event.code == joystick_map['move_x']):
                    seen_x = True
                    sx_val = event.state
                elif (event.code == joystick_map['move_y']):
                    seen_y = True
                    sy_val = event.state
                if (seen_x and seen_y):
                    seen_x = False
                    seen_y = False
                    if (event.state < -dead_zone or event.state > dead_zone):
                        click_drag_mouse(sx_val, sy_val)
                    else:
                        joy_held = False
                        pyautogui.mouseUp()
            elif (event.code == joystick_map['char_ud']):
                if (event.state == -1):
                    switch_char('u', event.state)
                elif (event.state == 1):
                    switch_char('d', event.state)
                else:
                    switch_char('z', event.state)
            else:
                try:
                    press(event.code, event.state)
                except KeyError:
                    print('Button not yet supported!')

if __name__ == '__main__':
    print('Starting')
    reset_mouse()
    try:
        joystick = inputs.devices.gamepads[0]
    except Exception:
        print('No joystick found!')
        exit()
    print('Using', joystick)
    pyautogui.PAUSE = 1 / refresh_hz
    pyautogui.FAILSAFE = True
    print('Running...')
    while True:
        update(joystick)