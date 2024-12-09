import sys
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import MSFluentWindow
from qfluentwidgets import FluentIcon as FIF

from home_interface import HomeInterface
from setting_interface import SettingInterface

logging.basicConfig(level=logging.INFO)


class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.settingInterface = SettingInterface(self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页')
        self.addSubInterface(self.settingInterface, FIF.SETTING, "设置")
        self.navigationInterface.setCurrentItem(
            self.homeInterface.objectName())

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('哔哩哔哩评论区抽奖工具')

        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.setStyleSheet("""
            SettingInterface, #scrollWidget {
                background-color: transparent;
            }

            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
