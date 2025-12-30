import json
import os

from platformdirs import user_data_dir

from light_control.constants import APP_NAME, APP_AUTHOR, SETTINGS_FILE, DEFAULT_COLOR


class StoredSettings:

    def __init__(self):
        self.data_dir = user_data_dir(APP_NAME, APP_AUTHOR)
        self.settings_path = os.path.join(self.data_dir, SETTINGS_FILE)
        self.session_color = None
        os.makedirs(self.data_dir, exist_ok=True)

    def get_color(self) -> tuple:
        if self.session_color is not None:
            return self.session_color

        if not os.path.exists(self.settings_path):
            self.session_color = DEFAULT_COLOR
            return self.session_color

        with open(self.settings_path, "r") as f:
            self.session_color = tuple(json.load(f)["static_color"])
            return self.session_color

    def save_color(self, color_hex: tuple[int, int, int]) -> None:
        with open(self.settings_path, "w") as f:
            json.dump({"static_color": color_hex}, f)
            self.session_color = color_hex
