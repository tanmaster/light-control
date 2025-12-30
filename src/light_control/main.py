import sys
from typing import Any

from PySide6.QtCore import QRunnable, QThreadPool, QTimer
from PySide6.QtGui import QIcon, QPixmap, QColor
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QColorDialog
from usbx import usb

from light_control.constants import APP_NAME, DEVICE_ID
from light_control.hid_light import HIDLight
from light_control.listener import LEDConnectedListener


class ColorChangeWorker(QRunnable):
    """ Task that runs in the background thread """

    def __init__(self, color_hex, hid_light: HIDLight):
        super().__init__()
        self.color_hex = color_hex
        self.hid_light = hid_light

    def run(self):
        self.hid_light.send_static(self.color_hex)


class LightControlApplication:
    def __init__(self, hid_light: HIDLight) -> None:
        self.hid_light = hid_light

        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APP_NAME)
        self.app.setApplicationDisplayName(APP_NAME)
        self.app.setQuitOnLastWindowClosed(False)
        self.thread_pool = QThreadPool.globalInstance()  # Manage background threads

        # 1. Setup Debounce Timer (waits 100ms after last move before executing)
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.execute_color_change)
        self.pending_color = (0xff, 0xff, 0xff)

        # 2. Setup Dialog
        self.dialog = QColorDialog()
        self.dialog.setWindowTitle(APP_NAME)
        self.dialog.setOption(QColorDialog.DontUseNativeDialog)
        self.dialog.currentColorChanged.connect(self.on_color_changed)

        # 3. Setup Tray
        self.tray = QSystemTrayIcon(self.create_icon(), self.app)

        menu = QMenu()
        menu.addAction("Open Picker", self.open_picker)
        menu.addAction("Quit", self.app.quit)
        self.tray.setContextMenu(menu)
        self.tray.show()

    def open_picker(self) -> None:
        # 1. Make the dialog visible
        self.dialog.show()

        # 2. Specifically for macOS: Raise it above other apps
        self.dialog.raise_()

        # 3. Give it keyboard and mouse focus
        self.dialog.activateWindow()

    def on_color_changed(self, color) -> None:
        """ This is called on the UI thread; keep it fast! """
        self.pending_color = color.red(), color.green(), color.blue()
        self.tray.setIcon(self.create_icon())
        # Restart timer: only executes if user stops moving for n milliseconds
        self.debounce_timer.start(5)

    def execute_color_change(self) -> None:
        """ Runs when timer finishes; launches the background worker """
        if self.pending_color:
            worker = ColorChangeWorker(self.pending_color, self.hid_light)
            self.thread_pool.start(worker)

    def run(self) -> Any:
        sys.exit(self.app.exec())

    def create_icon(self) -> QIcon:
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor.fromRgb(*self.pending_color))
        return QIcon(pixmap)


if __name__ == "__main__":
    # for some reason this needs to be called in order for usb notifications to work
    devices = usb.find_devices()

    hid_light = HIDLight()
    app = LightControlApplication(hid_light)

    listener = LEDConnectedListener(
        **DEVICE_ID,
        callback=app.execute_color_change
    )

    usb.on_connected(listener.handler)
    app.run()
