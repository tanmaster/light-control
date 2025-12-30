from usbx import Device


class LEDConnectedListener:
    def __init__(self, vendor_id, product_id, callback):
        self.vid = vendor_id
        self.pid = product_id
        self.callback = callback

    def handler(self, device: Device) -> None:
        # This callback runs in the USBX background thread
        if device.vid == self.vid and device.pid == self.pid:
            # Perform your non-UI logic here (e.g., database update, file log, etc.)
            self.callback()
