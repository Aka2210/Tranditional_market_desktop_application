import json
import os
from PySide6.QtWidgets import (QMainWindow, QLineEdit, QWidget, QHBoxLayout,
    QPushButton, QMessageBox, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QLabel, QCalendarWidget)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction
from lib.main_ui import Ui_MainWindow
from lib.fixedRentEditor import FixedRentEditor
from lib.func import load_json, AddNewRow, exportToJsonDict, loadCurrentDateRows, onDateChanged
from lib.moneyCalculate import RentSummaryInputDialog, RentSummaryPreview
from lib.bindingCode import NameBindingDialog
from lib.dateViewer import DateViewer
from lib.personSummary import PersonSummaryDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.calendar = self.ui.calendarWidget
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        
        # 初始化選單
        self.init_menu()
        
        self.rowContainer = self.ui.scrollAreaWidgetContents_2
        self.scrollAreaLayout = self.ui.verticalLayout_4
        self.rowsManager = []
        self.ui.addColumn.clicked.connect(lambda _: AddNewRow(self))
        self.ui.addColumn.setShortcut(Qt.Key_Space)
        self.ui.fixedRent.triggered.connect(self.openFixedRentEditor)
        self.current_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.calendar.clicked.connect(lambda date: onDateChanged(self, date))
        self.data_path = "resources/jsonData/mainData.json"
        self.data_dict = load_json(self.data_path)
        loadCurrentDateRows(self)
        self.ui.moneyCalculate.triggered.connect(self.openRentSummary)
        self.ui.bindingCode.triggered.connect(self.openNameBinding)
        
        # Add date viewer button
        self.date_viewer_btn = QPushButton("檢視日期資料", self)
        self.date_viewer_btn.clicked.connect(self.openDateViewer)
        self.menuBar().setCornerWidget(self.date_viewer_btn, Qt.TopLeftCorner)

    def openRentSummary(self):
        exportToJsonDict(self, self.current_date)
        dialog = RentSummaryInputDialog()
        if dialog.exec():
            owner, user, year, month = dialog.get_inputs()
            preview = RentSummaryPreview(owner=owner, user=user, year=year, month=month)
            preview.exec()

    def openFixedRentEditor(self):
        exportToJsonDict(self, self.current_date)
        self.fixedWindow = FixedRentEditor()
        self.fixedWindow.show()

    def openNameBinding(self):
        exportToJsonDict(self, self.current_date)
        self.nameBindingWindow = NameBindingDialog()
        self.nameBindingWindow.show()

    def openDateViewer(self):
        exportToJsonDict(self, self.current_date)
        self.dateViewer = DateViewer(self.data_path)
        self.dateViewer.show()

    def openPersonSummary(self):
        exportToJsonDict(self, self.current_date)
        self.personSummary = PersonSummaryDialog(self.data_path)
        self.personSummary.show()

    def init_menu(self):
        """初始化選單功能"""
        report_menu = self.menuBar().addMenu("報表")
        
        # 個人收支總結
        person_summary_action = QAction("個人收支總結", self)
        person_summary_action.triggered.connect(self.openPersonSummary)
        report_menu.addAction(person_summary_action)
        
    def closeEvent(self, event):
        exportToJsonDict(self, self.current_date)
        msg = QMessageBox(self)
        msg.setWindowTitle("是否離開？")
        yes_btn = msg.addButton("是", QMessageBox.ButtonRole.YesRole)
        no_btn = msg.addButton("否", QMessageBox.ButtonRole.NoRole)
        msg.exec()

        if msg.clickedButton() == yes_btn:
            event.accept()
        elif msg.clickedButton() == no_btn:
            event.ignore()
