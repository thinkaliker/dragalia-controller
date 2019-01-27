# Dragalia-Controller

This is a Python 3.7 script which enables using a controller to control the mobile game Dragalia Lost on Android without an emulator by using scrcpy.

[Video Demo!](https://www.youtube.com/watch?v=y3Dm4DJzWeU)

## Requirements

- Android device
- [scrcpy](https://github.com/Genymobile/scrcpy)
- Xbox One/360 controller
- Python 3.7+ (with pip)

## First Time Setup

1. Make sure you have all of the requirements fulfilled and you know how to use/run each one.
1. Run `pip install pyautogui`
1. Run `pip install inputs`
1. Adjust button coordinates as needed.

## Running

1. Start scrcpy.
1. Connect your controller of choice.
1. Run `python dragalia-controller.py`
1. Maximize scrcpy.
1. Sit back and enjoy using your controller to play!
1. Press ctrl+c a few times to quit.

## Defaults (my setup)

- OS: Windows 10
- Monitor size: 1920x1080
- Phone resolution: 1080x1920
- Dragalia Lost: Right Hand Mode, Quick90 off, Quick180 off

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
- Different DPI scaling support
- Different devices (find an easier way? relative screen boundaries vs exact screen boundaries?)
- Automatic detection of which menu you're in and switch input schemes automatically (inputs may be able to do detection)
- Sticker menu (find a button combo)

### Dragalia Lost is copyright Nintendo, Cygames.