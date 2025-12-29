import sys

from PySide6.QtGui import QIcon, QAction, QPixmap, QColor
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QColorDialog

from light_control.hidusb import send_static


class LiveColorPicker:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # 1. Create the persistent Color Dialog
        self.dialog = QColorDialog()
        self.dialog.setOption(QColorDialog.DontUseNativeDialog)  # Ensures live signals

        # 2. Connect the LIVE signal
        self.dialog.currentColorChanged.connect(self.on_color_live)

        # 3. Setup Tray
        self.tray = QSystemTrayIcon(self.create_icon("red"), self.app)
        menu = QMenu()

        pick_action = QAction("Open Live Picker", menu)
        pick_action.triggered.connect(self.dialog.show)
        menu.addAction(pick_action)

        menu.addSeparator()
        menu.addAction("Quit", self.app.quit)

        self.tray.setContextMenu(menu)
        self.tray.show()

    def on_color_live(self, color):
        """ This executes IMMEDIATELY as you move the mouse in the picker """
        hex_code = color.name()
        # Update tray icon color live as an example
        self.tray.setIcon(self.create_icon(hex_code))
        send_static((color.red(), color.green(), color.blue()))

    @staticmethod
    def create_icon(color_name):
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor(color_name))
        return QIcon(pixmap)

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    picker = LiveColorPicker()
    picker.run()
