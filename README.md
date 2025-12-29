# light-control

Attempting to reverse engineer the DX-Light App to control a generic monitor backlight strip.

### installation

install uv based on platform (command below is for macOS, for others
see https://github.com/astral-sh/uv?tab=readme-ov-file#installation)

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```shell
uv run python src/light_control/main.py # run it
```


#### todo
- autostart application
- store last application state (i.e. last set color) (also inbetween executions)
- remove custom color capability from color picker
- matter control?
- automatically detect when device is attached and re-execute last known color

- actually add this device to the openRGB project and make this project obsolete