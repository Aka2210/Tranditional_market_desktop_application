import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSpacerItem, QSizePolicy, QCalendarWidget
)
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QIcon
from lib.func import load_json, AddNewRow, exportToJsonDict, loadCurrentDateRows, onDateChanged

class FixedRentEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("固定位租修改")
        self.resize(800, 1000)
        self.rowsManager = []
        self.current_date = QDate.currentDate().toString("yyyy-MM-dd")
        self.data_path = "resources/jsonData/fixedRentData.json"
        self.data_dict = load_json(self.data_path)

        self.main_layout = QVBoxLayout(self)

        # 日期選擇器
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(lambda date: onDateChanged(self, date))
        self.main_layout.addWidget(self.calendar, alignment=Qt.AlignTop)

        # 標題列
        self.header = QWidget()
        header_layout = QHBoxLayout(self.header)
        headers = ["市場", "租金", "所有人", "使用人", "備註"]
        for name in headers:
            label = QLabel(name)
            label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(label)
        self.main_layout.addWidget(self.header)

        # ScrollArea 區域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.rowContainer = QWidget()
        self.scrollAreaLayout = QVBoxLayout(self.rowContainer)
        self.scroll_area.setWidget(self.rowContainer)
        self.main_layout.addWidget(self.scroll_area)

        # Spacer 防止 row 黏底
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scrollAreaLayout.addItem(self.verticalSpacer)

        # 控制列（新增按鈕 + 關閉按鈕）
        self.button_row = QWidget()
        btn_layout = QHBoxLayout(self.button_row)
        self.add_button = QPushButton("新增欄位")
        self.close_button = QPushButton("關閉")
        btn_layout.addWidget(self.add_button)
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_button)
        self.main_layout.addWidget(self.button_row)

        # 功能綁定
        self.add_button.clicked.connect(lambda: AddNewRow(self))
        self.close_button.clicked.connect(self.close)

        # 初始讀取資料
        loadCurrentDateRows(self)

    def closeEvent(self, event):
        exportToJsonDict(self, self.current_date)
        event.accept()