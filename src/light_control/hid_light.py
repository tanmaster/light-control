import time

import hid

from light_control.constants import (
    DEVICE_ID,
    RGB_INDEX,
    REPORT_ID_PREFIX,
    GENERIC_STATIC_COLOR_COMMAND,
)


class DisconnectedError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class HIDLight:
    def __init__(self):
        self.dev = hid.device()
        self.__try_open__()

    def send_static(self, rgb: tuple[int, int, int]) -> None:
        data_to_send = GENERIC_STATIC_COLOR_COMMAND.copy()
        data_to_send[RGB_INDEX] = rgb

        if not self.__try_send__(data_to_send):
            time.sleep(1)
            self.dev.close()
            self.__try_open__()
            self.__try_send__(data_to_send)

    def __try_send__(self, data_to_send: list[int]) -> bool:
        try:
            result = self.dev.write(REPORT_ID_PREFIX + data_to_send)
            if result == -1:
                raise DisconnectedError(
                    "Device was connected at some point but is no more"
                )
        except ValueError:
            return False
        except IOError:
            return False
        except DisconnectedError:
            return False

        return True

    def __try_open__(self):
        try:
            self.dev.open(**DEVICE_ID)
        except IOError:
            print("Device not found")
