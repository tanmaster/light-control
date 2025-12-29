APP_NAME="light-control"

# needed to identify the USB HID device
VENDOR_ID: int = 0x1a86
PRODUCT_ID: int = 0xfe07

DEVICE_ID: dict = {
    "vendor_id": VENDOR_ID,
    "product_id": PRODUCT_ID,
}

# The official driver increments these bytes with each command, though it seems that the Light strip does not really
# care about them. Thus, I set them to a constant value.
CNT_BYTE_1 = 0x01  # range from 0x01 to 0xfe, both inclusive
CNT_BYTE_2 = 0x00  # range from 0x00 to 0xff, both inclusive

# Start sequence, seems to be always the same in 'static color mode'
# At least in 'sync mode', this sequence differs
STATIC_COLOR_START_SEQUENCE = [0x52, 0x42, 0x10]

# This sequence defines the color. Used to bring the list to the right length, otherwise overwritten later when a color
# is picked.
RGB_SEQUENCE = [0xff, 0xff, 0xff]

# Bytes 6-8 represent the RGB values of GENERIC_STATIC_COLOR_COMMAND
RGB_INDEX = slice(6, 8)

# Appended to the end of the command to give it a length of 64 bytes.
ZERO_PADDING_SEQUENCE = [
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0,
]

# I am unsure what these two sequences represent, and whether they're only used in 'static color mode'
UNKNOWN_SEQUENCE_1 = [0x86, 0x1]
UNKNOWN_SEQUENCE_2 = [0x50, 0x51, 0x0, 0x0, 0x0, 0xfe]

GENERIC_STATIC_COLOR_COMMAND: list[int] = [
    *STATIC_COLOR_START_SEQUENCE,
    CNT_BYTE_1,
    *UNKNOWN_SEQUENCE_1,
    *RGB_SEQUENCE,
    *UNKNOWN_SEQUENCE_2,
    CNT_BYTE_2,
    *ZERO_PADDING_SEQUENCE,
]

# Required on Windows machines when using hidapi (seemingly optional on other platforms)
REPORT_ID_PREFIX = [0x00]
