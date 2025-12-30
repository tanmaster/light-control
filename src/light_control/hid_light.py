import time

import hid

from light_control.constants import DEVICE_ID, RGB_INDEX, REPORT_ID_PREFIX, GENERIC_STATIC_COLOR_COMMAND


class HIDLight:

    def __init__(self):
        self.dev = hid.device()
        self.dev.open(**DEVICE_ID)

    # called when disconnected / reconnected
    def reopen(self):
        self.dev.close()
        self.dev.open(**DEVICE_ID)

    def send_static(self, rgb: tuple[int, int, int]) -> None:
        data_to_send = GENERIC_STATIC_COLOR_COMMAND.copy()
        data_to_send[RGB_INDEX] = rgb

        # Add a Report ID prefix (0x00)
        result = self.dev.write(REPORT_ID_PREFIX + data_to_send)
        if result == -1:
            # try again once after waiting a bit
            time.sleep(1)
            self.reopen()
            self.dev.write(REPORT_ID_PREFIX + data_to_send)
