import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSpacerItem, QSizePolicy, QCalendarWidget, QMessageBox
)
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QKeySequence
from PySide6.QtGui import QIcon
from lib.func import load_json, AddNewRow, exportToJsonDict, loadCurrentDateRows, onDateChanged

class FixedRentEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("固定位租修改")
        self.resize(600, 800)
        self.rowsManager = []
        self.current_date = QDate.currentDate().toString("yyyy-MM-dd")
        self.data_path = "resources/jsonData/fixedRentData.json"
        self.data_dict = load_json(self.data_path)

        self.main_layout = QVBoxLayout(self)

        # 日期選擇器
        self.calendar = QCalendarWidget()
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
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

        # 控制列（新增按鈕 + 關閉按鈕 + 複製上月資料）
        self.button_row = QWidget()
        btn_layout = QHBoxLayout(self.button_row)
        self.add_button = QPushButton("新增欄位")
        self.copy_button = QPushButton("複製上月資料")
        self.close_button = QPushButton("關閉")
        btn_layout.addWidget(self.add_button)
        btn_layout.addWidget(self.copy_button)
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_button)
        self.main_layout.addWidget(self.button_row)

        # 功能綁定
        self.add_button.clicked.connect(lambda: AddNewRow(self))
        self.add_button.setShortcut(Qt.Key_Space)
        self.copy_button.clicked.connect(self.copyLastMonthData)
        self.close_button.clicked.connect(self.close)

    def copyLastMonthData(self):
        """將上個月的所有資料複製到當前月份"""
        current_date = QDate.fromString(self.current_date, "yyyy-MM-dd")
        last_month = current_date.addMonths(-1)
        
        # 取得上個月的第一天和最後一天
        first_day = QDate(last_month.year(), last_month.month(), 1)
        last_day = QDate(last_month.year(), last_month.month(), last_month.daysInMonth())
        
        copied_dates = 0
        current_day = first_day
        while current_day <= last_day:
            date_str = current_day.toString("yyyy-MM-dd")
            if date_str in self.data_dict:
                # 計算對應的當前月份日期
                target_date = current_day.addMonths(1).toString("yyyy-MM-dd")
                self.data_dict[target_date] = self.data_dict[date_str].copy()
                copied_dates += 1
            current_day = current_day.addDays(1)
        
        if copied_dates > 0:
            QMessageBox.information(self, "成功", f"已複製上個月 {copied_dates} 天的資料到當前月份")
        else:
            QMessageBox.warning(self, "警告", "上個月沒有任何資料可複製")

        # 初始讀取資料
        loadCurrentDateRows(self)

    def closeEvent(self, event):
        exportToJsonDict(self, self.current_date)
        event.accept()
