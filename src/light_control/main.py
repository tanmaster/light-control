import sys
from typing import Any

from PySide6.QtCore import QRunnable, QThreadPool, QTimer, Slot
from PySide6.QtGui import QIcon, QPixmap, QColor, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QColorDialog
from light_control.constants import APP_NAME, DEVICE_ID
from light_control.hid_light import HIDLight
from light_control.listener import LEDConnectedListener
from light_control.settings import StoredSettings
from usbx import usb


class ColorChangeWorker(QRunnable):
    """ Task that runs in the background thread """

    def __init__(self, color_hex, light: HIDLight, settings: StoredSettings) -> None:
        super().__init__()
        self.color_hex = color_hex
        self.light = light
        self.settings = settings

    def run(self) -> None:
        self.settings.save_color(self.color_hex)
        self.light.send_static(self.color_hex)


class LightControlApplication:
    def __init__(self, light: HIDLight, settings: StoredSettings) -> None:
        self.light = light
        self.settings = settings

        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APP_NAME)
        self.app.setApplicationDisplayName(APP_NAME)
        self.app.setQuitOnLastWindowClosed(False)
        self.thread_pool = QThreadPool.globalInstance()  # Manage background threads

        # 1. Setup Debounce Timer (waits after last move before executing)
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.execute_color_change)
        self.pending_color = settings.get_color()
        self.execute_color_change()  # set the initial color to the stored or default one

        # 2. Setup Dialog
        self.dialog = QColorDialog()
        self.dialog.setWindowTitle(APP_NAME)
        self.dialog.setOption(QColorDialog.DontUseNativeDialog)
        self.dialog.setCurrentColor(QColor.fromRgb(*self.pending_color))
        self.dialog.currentColorChanged.connect(self.on_color_changed)

        # 3. Setup Tray
        self.tray = QSystemTrayIcon(self.create_icon(), self.app)
        # self.tray.activated.connect(self.on_tray_activated)

        menu = QMenu()
        self.status_action = QAction(f"Device Status: {self.light.status}", menu)
        self.status_action.setEnabled(False)  # This makes it non-interactive
        menu.addAction(self.status_action)
        menu.addAction("Open Picker", self.open_picker)
        menu.addSeparator()
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
            worker = ColorChangeWorker(self.pending_color, self.light, self.settings)
            self.thread_pool.start(worker)

    @Slot(str)
    def update_status(self, new_status) -> None:
        self.status_action.setText(f"Device Status: {new_status}")

    def run(self) -> Any:
        sys.exit(self.app.exec())

    def create_icon(self) -> QIcon:
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor.fromRgb(*self.pending_color))
        return QIcon(pixmap)


if __name__ == "__main__":
    # for some reason this needs to be called in order for usb notifications to work
    devices = usb.find_devices()

    # initialize dependencies
    stored_settings = StoredSettings()
    hid_light = HIDLight()

    app = LightControlApplication(hid_light, stored_settings)

    hid_light.status_changed.connect(app.update_status)
    # listener for usb changes (plug in, plug out)
    listener = LEDConnectedListener(
        **DEVICE_ID,
        callback_fn=app.execute_color_change
    )
    usb.on_connected(listener.handler)

    app.run()
