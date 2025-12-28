import hid

from light_control.constants import VENDOR_ID, PRODUCT_ID, COLOR_BLUE

device = {
    "vendor_id": VENDOR_ID,
    "product_id": PRODUCT_ID,
}

dev = hid.device()
dev.open(**device)  # use your vid/pid

data_to_send = COLOR_BLUE
# data_to_send = COLOR_WARM_WHITE

# Add a Report ID prefix (0x00) (required on Windows, optional for macOS, ? for linux)
dev.write([0x00] + data_to_send)
