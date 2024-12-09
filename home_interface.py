import random
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QTableWidgetItem

from qfluentwidgets import (
    PrimaryPushButton, TextEdit, TableWidget, MessageBox, PrimaryPushSettingCard,
    InfoBar, InfoBarPosition, HyperlinkCard
)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QFileDialog, QAbstractItemView

from har_parser import get_all_uid_with_name_comments

HAR_HELP_URL = "https://github.com/dreamhunter2333/bilibili-comments-lucky-draw"


class HomeInterface(QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.tokenLineEdit = TextEdit(self)
        self.tokenLineEdit.setPlaceholderText('请输入排除的用户UID, 每行一个')
        self.tokenLineEdit.setFixedHeight(60)
        self.button = PrimaryPushButton('开始抽奖', self)
        self.button.clicked.connect(self.__onButtonClicked)
        self.harHelpCard = HyperlinkCard(
            HAR_HELP_URL,
            "打开帮助文档",
            FIF.HELP,
            "如何获取 HAR 文件 进行抽奖",
            parent=self
        )
        self.harFileCard = PrimaryPushSettingCard(
            "选择文件",
            FIF.DOCUMENT,
            "HAR 文件路径",
            parent=self
        )
        self.harFileCard.clicked.connect(self.__onHarFileCardClicked)

        self.table = TableWidget(self)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.harHelpCard)
        self.vBoxLayout.addWidget(self.harFileCard)
        self.vBoxLayout.addWidget(self.tokenLineEdit)
        self.vBoxLayout.addWidget(self.button)
        self.vBoxLayout.addWidget(self.table)
        self.setObjectName('HomeInterface')

        # 启用边框并设置圆角
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setColumnCount(3)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置水平表头并隐藏垂直表头
        self.table.setHorizontalHeaderLabels(
            ['UID', 'NAME', 'COMMENTS'])
        # self.table.verticalHeader().hide()
        self.data = []

    def __onHarFileCardClicked(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, self.tr("选择 har 文件"), "./", "har 文件(*.har)",
                options=QFileDialog.Options() | QFileDialog.ReadOnly
            )
            if not file_path:
                InfoBar.warning(
                    title='',
                    content='未选择文件',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
                return
            self.harFileCard.setContent(file_path)
            self.data = get_all_uid_with_name_comments(file_path)
            self.table.setRowCount(len(self.data))

            for i, line in enumerate(self.data):
                for j, content in enumerate(line):
                    self.table.setItem(i, j, QTableWidgetItem(content))
            self.table.resizeColumnsToContents()
            InfoBar.success(
                title='',
                content='成功从 har 文件中提取数据',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        except Exception as e:
            logging.exception(e)
            InfoBar.error(
                title='错误',
                content=f"{e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

    def __onButtonClicked(self):
        try:
            exclude_uids = self.tokenLineEdit.toPlainText().split('\n')
            exclude_uids = tuple(
                uid.strip() for uid in exclude_uids if uid.strip()
            )
            target_uids = {
                line[0].strip(): line[1].strip()
                for line in self.data
                if line[0].strip() not in exclude_uids
            }
            if not target_uids:
                InfoBar.warning(
                    title='',
                    content='没有可抽奖的用户',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
                return
            lucky_uid = random.choice(list(target_uids.keys()))
            lucky_uid_comments = "\r\n评论: ".join([
                line[2]
                for line in self.data if line[0] == lucky_uid
            ][:10])
            w = MessageBox(
                "恭喜中奖",
                (
                    f"UID: {lucky_uid}"
                    f"\r\n昵称: {target_uids[lucky_uid]}"
                    f"\r\n评论: {lucky_uid_comments}"
                ),
                self
            )
            w.cancelButton.hide()
            w.exec_()
        except Exception as e:
            logging.exception(e)
            InfoBar.error(
                title='错误',
                content=f"{e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
