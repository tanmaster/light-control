import hid
import platform

from light_control.constants import VENDOR_ID, PRODUCT_ID, COLOR_BLUE, COLOR_WARM_WHITE

device = {
    "vendor_id": VENDOR_ID,
    "product_id": PRODUCT_ID,
}

dev = hid.device()
dev.open(**device)  # use your vid/pid

data_to_send = COLOR_BLUE
# data_to_send = COLOR_WARM_WHITE

# Add a Report ID prefix (0x00) for Windows
if platform.system() == "Windows":
    data_to_send = [0x00] + data_to_send

dev.write(data_to_send)
