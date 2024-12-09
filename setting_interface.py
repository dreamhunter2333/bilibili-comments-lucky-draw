# coding:utf-8
import logging
import os
from datetime import datetime
from qfluentwidgets import (
    qconfig, QConfig, SettingCardGroup, OptionsSettingCard, HyperlinkCard,
    PrimaryPushSettingCard, LargeTitleLabel, ExpandLayout, setTheme, ScrollArea,
    InfoBar, InfoBarPosition
)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


# load config for user configuration path
config_path = os.path.join(
    os.path.expanduser('~'), '.bili-lucky-draw/config.json'
)
cfg = QConfig()
qconfig.load(config_path, cfg)

HELP_URL = "https://github.com/dreamhunter2333/bilibili-comments-lucky-draw"
RELEASE_URL = "https://github.com/dreamhunter2333/bilibili-comments-lucky-draw/releases"
AUTHOR = "撑伞君"
VERSION = "v0.0.1"


class SettingInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = LargeTitleLabel("设置", self)
        # personalization
        self.personalGroup = SettingCardGroup("个性化", self.scrollWidget)
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            "应用主题",
            "调整你的应用外观",
            texts=["浅色", "深色", "跟随系统设置"],
            parent=self.personalGroup
        )

        # application
        self.aboutGroup = SettingCardGroup("关于", self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            "帮助和反馈",
            FIF.HELP,
            "帮助和反馈",
            "前往帮助和反馈",
            self.aboutGroup
        )
        self.aboutCard = HyperlinkCard(
            RELEASE_URL,
            "检查更新",
            FIF.INFO,
            "关于",
            (
                f"© Copyright {datetime.now().year}, {AUTHOR}, "
                f"version: {VERSION}"
            ),
            self.aboutGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        # initialize layout
        self.__initLayout()
        cfg.themeChanged.connect(self.__setTheme)

    def __initLayout(self):
        self.settingLabel.move(20, 20)

        # add cards to group
        self.personalGroup.addSettingCard(self.themeCard)
        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(20, 10, 20, 0)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __setTheme(self, *args, **kwargs):
        try:
            setTheme(*args, **kwargs)
            InfoBar.success(
                title='',
                content="切换主题成功！",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        except Exception as e:
            logging.exception(e)
            InfoBar.error(
                title='',
                content=f"切换主题失败！{e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
