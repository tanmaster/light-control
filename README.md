# light-control

Attempting to reverse engineer the DX-Light App to control a generic monitor backlight strip.
This software will control a generic [light strip monitor backlight](https://www.amazon.de/dp/B0F53TVYZL) frequently
found on amazon.

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