import hid

from light_control.constants import DEVICE_ID, RGB_INDEX, REPORT_ID_PREFIX, GENERIC_COLOR_COMMAND

dev = hid.device()
dev.open(**DEVICE_ID)  # use your vid/pid


def send_static(rgb: tuple[int, int, int]) -> None:
    data_to_send = GENERIC_COLOR_COMMAND.copy()
    data_to_send[RGB_INDEX] = rgb

    # Add a Report ID prefix (0x00) (required on Windows, optional for macOS, ? for linux)
    dev.write(REPORT_ID_PREFIX + data_to_send)
