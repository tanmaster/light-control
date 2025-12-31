# light-control

Attempting to reverse engineer the DX-Light App to control a generic monitor backlight strip.
This software will control a generic [light strip monitor backlight](https://www.amazon.de/dp/B0F53TVYZL) frequently
found on amazon.

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