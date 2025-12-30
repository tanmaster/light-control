from usbx import Device


class LEDConnectedListener:

    def __init__(self, vendor_id, product_id, callback_fn):
        self.__vid__ = vendor_id
        self.__pid__ = product_id
        self.__led_connected_callback__ = callback_fn

    def handler(self, device: Device) -> None:
        # This callback runs in the USBX background thread
        if device.vid == self.__vid__ and device.pid == self.__pid__:
            # Perform your non-UI logic here (e.g., database update, file log, etc.)
            self.__led_connected_callback__()
