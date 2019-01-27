# Dragalia-Controller

This is a Python 3.7 script which enables using a controller to control the mobile game Dragalia Lost on Android without an emulator by using scrcpy.

## Requirements
- Android device
- [scrcpy](https://github.com/Genymobile/scrcpy)
- XBox One/360 controller
- Python 3.7+ (with pip)

## First Time Setup
1. Make sure you have all of the requirements fulfilled and you know how to use/run each one.
1. Run `pip install pyautogui`
1. Run `pip install inputs`
1. Adjust button coordinates as needed.

## Running
1. Start scrcpy.
1. Connect your controller of choice.
1. Run `python dragalia_lost.py`
1. Maximize scrcpy.
1. Sit back and enjoy using your controller to play!

## Defaults
- OS: Windows 10
- Monitor size: 1920x1080
- Phone resolution: 1080x1920
- Dragalia Lost: Right Hand Mode, Quick90 off, Quick180 off

### Default Key mappings for XBox One/360
Button | Action
--|--------
A | Attack (tap)
X | First skill
Y | Second skill
B | Third skill
LB | Dragon
RB | Helper skill
Left Joystick | Move
Menu | Pause
Select | Minimap
DPad Up/Down | Switch character up/down

## TODO/Nice to haves
- Better joystick input handling (something's off about deadzone detection)
- Multiple controller support (PlayStation, etc)
- Different DPI scaling support
- Different devices (find an easier way? relative screen boundaries vs exact screen boundaries?)