# Dragalia-Controller

This is a Python 3.7 script which enables using a controller to control the mobile game Dragalia Lost on Android without an emulator by using scrcpy.

[Video Demo!](https://www.youtube.com/watch?v=y3Dm4DJzWeU)

## Requirements

- Android device
- Latest [scrcpy](https://github.com/Genymobile/scrcpy)
- Xbox One/360 controller
- Python 3.7+ (with pip)
- PyAutoGUI
- PyInputs
- PyWin32

## First Time Setup

1. Make sure you have all of the requirements fulfilled and you know how to use/run each one.
1. Run `pip install pyautogui`
1. Run `pip install inputs`
1. Run `pip install pywin32`
1. Clone this repository to anywhere on your computer.
1. Adjust button ratios as needed.
1. Adjust the following constants

Constant | Default value
--|--
WINDOW_TITLE | 'Pixel 2' (this should be the title of the scrcpy display window)
UI_LAYOUT | 'right' ('right' or 'left' UI Layout)
TITLE_OFFSET | 30 (Thickness of your Windows titlebar - affected by Windows scaling)

## Running

1. Start scrcpy, preferrably with the window title.
1. Connect your controller of choice.
1. Run `python dragalia-controller.py`
1. Keep the window at the same aspect ratio without black bars if you need to resize it.
1. Sit back and enjoy using your controller to play!
1. Press ctrl+c a few times to quit.

## Defaults (my setup)

- OS: Windows 10
- Windows Display scaling: 100%
- Monitor size: 1920x1080, 24"
- Phone resolution: 1080x1920, Pixel 2
- Dragalia Lost: Quick90 off, Quick180 off

### Default Key mappings for Xbox One/360

Button | Action
--|--------
A | Attack (tap)
X | First skill
Y | Second skill
B | Third skill
LB | Dragon
RB | Helper skill
Left Joystick | Move
Right Joystick | Dodge (Swipe)
Menu | Pause/unpause
Select | Minimap
DPad Up/Down | Switch character up/down

## Contributing

Please fork the repository, and make a pull request! Make sure to be as detailed as possible in your description - I'll probably accept it. All improvements are welcome!

## Bugs

There are lots of them, I'm sure (see below). If you find something though, please create an issue. Be as detailed as possible!

## TODO/Nice to haves

- Better joystick input handling (something's off about deadzone detection, especially on X-only and Y-only axes)
- Multiple controller support (PlayStation, etc)
- ~~Different DPI scaling support~~
- ~~Different devices (find an easier way? relative screen boundaries vs exact screen boundaries?)~~
- Automatic detection of which menu you're in and switch input schemes automatically (inputs may be able to do detection)
- Sticker menu (find a button combo)

### Dragalia Lost is copyright Nintendo, Cygames.
