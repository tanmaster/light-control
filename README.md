# light-control

Attempting to reverse engineer the DX-Light App to control a generic monitor backlight strip.
This software will control a generic [light strip monitor backlight](https://www.amazon.de/dp/B0F53TVYZL) frequently
found on amazon. Kudos go out
to [this reddit user](https://www.reddit.com/r/Fedora/comments/1nygjfu/chinese_noname_light_strip/nik3ven/) for the idea
of capturing usb packets via wireshark and replaying them.

### Features

- allows for setting a static color
- cross-platform
- program stays alive in system tray (can be exited and light should remain)
- uses a basic color picker
- persists selected color and reads it on next start
- auto-detects when the light is attached and re-executes last known color (useful when system is waking up from sleep)

### Limitations

At over 100MB unzipped, this project is admittedly large for its functionality. It was developed primarily as a personal
learning exercise rather than an optimized utility.

Future Plans:
I hope to eventually port the core functionality to OpenRGB, which is the more appropriate ecosystem for this tool.

For Contributors:
If you wish to integrate this protocol into other projects, the essential logic is contained within `constants.py` and
`hid_light.py` (approx. 100 lines of code). Those files include documentation on the USB HID byte sequences I
reversed-engineered.

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

uv will download all required dependencies and run `light-control`.

#### todo
- create proper releases on all platforms
- autostart application
- actually add this device to the openRGB project and make this project obsolete