# lib/func.py

import json
import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout,
    QPushButton, QMessageBox, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QLabel, QLineEdit)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class CustomLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.clearFocus()
        else:
            super().keyPressEvent(event)

def createLineEdit():
    return CustomLineEdit()

def load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 無法讀取 JSON: {e}")
        return {}

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 資料已儲存至 {path}")

def AddNewRow(self):
    row = QWidget(self.rowContainer)
    row.setObjectName("row")
    row_layout = QHBoxLayout(row)

    for i in range(5):
        line = createLineEdit()
        line.setObjectName(f"lineEdit_{i}")
        row_layout.addWidget(line)
        if i == 0:
            line.setFocus()

    btn_row = QWidget(self.rowContainer)
    btn_layout = QHBoxLayout(btn_row)
    button = QPushButton("", btn_row)
    button.setIcon(QIcon(":/images/x.png"))
    button.setIconSize(QSize(24, 24))
    button.setObjectName("button")
    btn_layout.addStretch()
    btn_layout.addWidget(button)

    count = self.scrollAreaLayout.count()
    self.scrollAreaLayout.insertWidget(count - 1, row)
    self.scrollAreaLayout.insertWidget(count, btn_row)

    button.clicked.connect(lambda _, r=row, b=btn_row: RemoveRow(self, r, b))
    self.rowsManager.append((row, btn_row))

def RemoveRow(self, row, btn_row):
    self.scrollAreaLayout.removeWidget(row)
    self.scrollAreaLayout.removeWidget(btn_row)
    row.deleteLater()
    btn_row.deleteLater()
    if (row, btn_row) in self.rowsManager:
        self.rowsManager.remove((row, btn_row))

def exportToJsonDict(self, date_str):
    result = []
    for row_widget, _ in self.rowsManager:
        row_data = []
        for child in row_widget.findChildren(QLineEdit):
            row_data.append(child.text())
        result.append(row_data)
    self.data_dict[date_str] = result
    save_json(self.data_dict, self.data_path)

def clearAllRows(self):
    for row, btn_row in self.rowsManager:
        self.scrollAreaLayout.removeWidget(row)
        self.scrollAreaLayout.removeWidget(btn_row)
        row.deleteLater()
        btn_row.deleteLater()
    self.rowsManager.clear()

def loadCurrentDateRows(self):
    clearAllRows(self)
    date_data = self.data_dict.get(self.current_date, [])
    for values in date_data:
        AddNewRow(self)
        row, _ = self.rowsManager[-1]
        edits = row.findChildren(QLineEdit)
        for i, text in enumerate(values):
            if i < len(edits):
                edits[i].setText(text)

def onDateChanged(self, date):
    exportToJsonDict(self, self.current_date)
    self.current_date = date.toString("yyyy-MM-dd")
    loadCurrentDateRows(self)
