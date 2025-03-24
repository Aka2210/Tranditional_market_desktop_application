from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QTabWidget, QWidget
)
from PySide6.QtCore import Qt
import json
import os

class NameBindingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("綁定設定")
        self.resize(450, 350)

        layout = QVBoxLayout(self)

        # 分頁容器
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # 名字綁定頁面
        self.name_tab = QWidget()
        self.name_layout = QVBoxLayout(self.name_tab)
        self.setup_binding_page(self.name_layout, "name_bindings.json", "代號，如：A100", "對應名稱，如：小明")
        self.tabs.addTab(self.name_tab, "名稱綁定")

        # 市場綁定頁面
        self.market_tab = QWidget()
        self.market_layout = QVBoxLayout(self.market_tab)
        self.setup_binding_page(self.market_layout, "market_bindings.json", "市場代號，如：S01", "對應名稱，如：第一市場")
        self.tabs.addTab(self.market_tab, "市場綁定")

        self.setLayout(layout)

    def setup_binding_page(self, layout, file_name, code_placeholder, name_placeholder):
        input_layout = QHBoxLayout()
        code_input = QLineEdit()
        code_input.setPlaceholderText(code_placeholder)
        name_input = QLineEdit()
        name_input.setPlaceholderText(name_placeholder)
        add_button = QPushButton("新增/更新")

        input_layout.addWidget(code_input)
        input_layout.addWidget(name_input)
        input_layout.addWidget(add_button)
        layout.addLayout(input_layout)

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["代號", "名稱", "操作"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(table)

        bindings_path = os.path.join("resources", "jsonData", file_name)
        bindings = self.load_bindings(bindings_path)

        def refresh_table():
            table.setRowCount(0)
            for row, (code, name) in enumerate(bindings.items()):
                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem(code))
                table.setItem(row, 1, QTableWidgetItem(name))
                delete_btn = QPushButton("刪除")
                delete_btn.clicked.connect(lambda _, c=code: delete_binding(c))
                table.setCellWidget(row, 2, delete_btn)

        def add_binding():
            code = code_input.text().strip()
            name = name_input.text().strip()
            if not code or not name:
                QMessageBox.warning(self, "輸入錯誤", "請輸入代號與名稱")
                return
            bindings[code] = name
            refresh_table()
            code_input.clear()
            name_input.clear()

        def delete_binding(code):
            if code in bindings:
                del bindings[code]
                refresh_table()

        def save():
            os.makedirs(os.path.dirname(bindings_path), exist_ok=True)
            with open(bindings_path, "w", encoding="utf-8") as f:
                json.dump(bindings, f, ensure_ascii=False, indent=2)

        add_button.clicked.connect(add_binding)
        refresh_table()
        layout.save = save  # 將保存函數掛載在 layout 上，供 closeEvent 使用

    def load_bindings(self, path):
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def closeEvent(self, event):
        # 分別呼叫每頁的 save 方法
        if hasattr(self.name_layout, "save"):
            self.name_layout.save()
        if hasattr(self.market_layout, "save"):
            self.market_layout.save()
        event.accept()