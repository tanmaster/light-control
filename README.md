# light-control

Attempting to reverse engineer the DX-Light App to control a generic monitor backlight strip.
This software will control a generic [light strip monitor backlight](https://www.amazon.de/dp/B0F53TVYZL) frequently
found on amazon. Kudos go out
to [this reddit user](https://www.reddit.com/r/Fedora/comments/1nygjfu/chinese_noname_light_strip/nik3ven/) for the idea
of capturing usb packets via wireshark and replaying them.

### Features

- allows for setting a static color
- program stays alive in system tray (can be exited and light should remain)
- uses a basic color picker
- persists selected color and reads it on next start
- auto-detects when the light is attached and re-executes last known color (useful when system is waking up from sleep)

### Limitations

I am aware that the unzipped project takes up more than 100MBs (I wouldn't want to run a program this large just to
control some LEDs myself), but this is not something I intend to change anymore. The project was rather a learning
opportunity for me. If I find time in the future, I intend to incorporate the basic functionality that this project
provides into [openRGB](https://openrgb.org/) (probably should have done that in the first place). In case anyone
stumbles upon this and wants to beat me to it: the 'meat' of the HID command can be found inside `constants.py` and
`hid_light.py` (~100 lines combined). There I also explain what (I think) I figured out about the byte sequence.

Disclaimer:
This software has been manually verified only on the specific hardware described above (Vendor ID: `0x1A86`, Product ID:
`0xFE07`, 80-LED variant). Use this tool at your own risk; transmitting raw byte commands to USB HID devices carries a
small but inherent risk of causing permanent hardware failure (bricking).

### installation

install uv based on platform (command below is for macOS, for others
see https://github.com/astral-sh/uv?tab=readme-ov-file#installation)

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

to run:

```shell
uv run python src/light_control/main.py
```

#### todo

- autostart application
- actually add this device to the openRGB project and make this project obsolete