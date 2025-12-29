import sys

from PySide6.QtCore import QRunnable, QThreadPool, QTimer
from PySide6.QtGui import QIcon, QPixmap, QColor
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QColorDialog
from light_control.constants import APP_NAME
from light_control.hidusb import send_static


class ColorChangeWorker(QRunnable):
    """ Task that runs in the background thread """

    def __init__(self, color_hex):
        super().__init__()
        self.color_hex = color_hex

    def run(self):
        send_static(self.color_hex)


class LightControlApplication:
    def __init__(self):
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

    def open_picker(self):
        # 1. Make the dialog visible
        self.dialog.show()

        # 2. Specifically for macOS: Raise it above other apps
        self.dialog.raise_()

        # 3. Give it keyboard and mouse focus
        self.dialog.activateWindow()

    def on_color_changed(self, color):
        """ This is called on the UI thread; keep it fast! """
        self.pending_color = color.red(), color.green(), color.blue()
        self.tray.setIcon(self.create_icon())
        # Restart timer: only executes if user stops moving for 100ms
        self.debounce_timer.start(5)

    def execute_color_change(self):
        """ Runs when timer finishes; launches the background worker """
        if self.pending_color:
            worker = ColorChangeWorker(self.pending_color)
            self.thread_pool.start(worker)

    def run(self):
        sys.exit(self.app.exec())

    def create_icon(self):
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor.fromRgb(*self.pending_color))
        return QIcon(pixmap)


if __name__ == "__main__":
    LightControlApplication().run()
