import sys

from PySide6.QtCore import QRunnable, QThreadPool, QTimer
from PySide6.QtGui import QIcon, QPixmap, QColor
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QColorDialog

from light_control.hidusb import send_static


class HeavyWorker(QRunnable):
    """ Task that runs in the background thread """

    def __init__(self, color_hex):
        super().__init__()
        self.color_hex = color_hex

    def run(self):
        send_static(self.color_hex)


class AsyncColorPicker:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.thread_pool = QThreadPool.globalInstance()  # Manage background threads

        # 1. Setup Debounce Timer (waits 100ms after last move before executing)
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.execute_heavy_task)
        self.pending_color = None

        # 2. Setup Dialog
        self.dialog = QColorDialog()
        self.dialog.setOption(QColorDialog.DontUseNativeDialog)
        self.dialog.currentColorChanged.connect(self.on_color_changed)

        # 3. Setup Tray
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor("gray"))
        self.tray = QSystemTrayIcon(QIcon(pixmap), self.app)

        menu = QMenu()
        menu.addAction("Open Picker", self.dialog.show)
        menu.addAction("Quit", self.app.quit)
        self.tray.setContextMenu(menu)
        self.tray.show()

    def on_color_changed(self, color):
        """ This is called on the UI thread; keep it fast! """
        self.pending_color = color.red(), color.green(), color.blue()
        # Restart timer: only executes if user stops moving for 100ms
        self.debounce_timer.start(100)

    def execute_heavy_task(self):
        """ Runs when timer finishes; launches the background worker """
        if self.pending_color:
            worker = HeavyWorker(self.pending_color)
            self.thread_pool.start(worker)

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    AsyncColorPicker().run()
