import sys

from PySide6.QtGui import QIcon, QAction, QPixmap, QColor
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QColorDialog

from light_control.hidusb import send_static


def pick_color():
    color = QColorDialog.getColor()
    if color.isValid():
        QApplication.clipboard().setText(color.name())
        send_static((color.red(), color.green(), color.blue()))
        # Notification to confirm it's working
        # tray.showMessage("Color Copied", f"Saved {color.name()} to clipboard", QSystemTrayIcon.Information)


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# Create a temporary 16x16 red icon so you can see it immediately
pixmap = QPixmap(16, 16)
pixmap.fill(QColor("red"))
icon = QIcon(pixmap)

tray = QSystemTrayIcon(icon, app)
menu = QMenu()

pick_action = QAction("Pick Color", menu)
pick_action.triggered.connect(pick_color)
menu.addAction(pick_action)

menu.addSeparator()

quit_action = QAction("Quit", menu)
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)

tray.setContextMenu(menu)
tray.show()

sys.exit(app.exec())
