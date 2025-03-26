import json
import os
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QComboBox, QPushButton, QMessageBox, QScrollArea,
                              QWidget, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QTextDocument
from lib.bindingCode import NameBindingDialog

class PersonSummaryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_paths = ["resources/jsonData/mainData.json", "resources/jsonData/fixedRentData.json"]
        self.setWindowTitle("個人收支總結")
        self.resize(600, 400)
        self.bindings = {}
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # 選擇人員
        self.person_combo = QComboBox()
        self.load_persons()
        layout.addWidget(QLabel("選擇人員:"))
        layout.addWidget(self.person_combo)
        
        # 創建滾動區域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # 創建內容容器
        self.content_widget = QWidget()
        self.content_layout = QGridLayout(self.content_widget)
        
        # 收入支出分兩欄
        self.income_label = QLabel("")
        self.income_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.expense_label = QLabel("")
        self.expense_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.content_layout.addWidget(QLabel("收入明細:"), 0, 0)
        self.content_layout.addWidget(self.income_label, 1, 0)
        self.content_layout.addWidget(QLabel("支出明細:"), 0, 1)
        self.content_layout.addWidget(self.expense_label, 1, 1)
        
        scroll.setWidget(self.content_widget)
        layout.addWidget(scroll)
        
        # 按鈕
        btn_layout = QHBoxLayout()
        self.calculate_btn = QPushButton("計算")
        self.calculate_btn.clicked.connect(self.calculate_summary)
        btn_layout.addWidget(self.calculate_btn)
        
        self.print_btn = QPushButton("列印")
        self.print_btn.clicked.connect(self.print_summary)
        btn_layout.addWidget(self.print_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
    def resolve_name(self, code):
        """根據代號解析實際名稱"""
        return self.bindings.get(code, code)
        
    def load_persons(self):
        """加載所有人員（包括使用人和所有人）"""
        try:
            # 從綁定文件加載人員
            binding_path = "resources/jsonData/name_bindings.json"
            if os.path.exists(binding_path):
                with open(binding_path, 'r', encoding='utf-8') as f:
                    self.bindings = json.load(f)
            else:
                self.bindings = {}
                    
            persons = set()
            
            # 從兩個數據源加載出現過的所有人
            for data_path in self.data_paths:
                if os.path.exists(data_path):
                    with open(data_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for month_data in data.values():
                            for entry in month_data:
                                if len(entry) > 2:
                                    if entry[2]:  # 使用人
                                        persons.add(self.resolve_name(entry[2]))
                                    if len(entry) > 3 and entry[3]:  # 所有人
                                        persons.add(self.resolve_name(entry[3]))
                                    
            # 按字母順序排序並添加到下拉框
            for person in sorted(persons):
                self.person_combo.addItem(person)
                
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"加載人員列表失敗: {str(e)}")
            
    def calculate_summary(self):
        """計算選定人員的總收支（合併兩個數據源）"""
        selected_person = self.person_combo.currentText()
        if not selected_person:
            return
            
        try:
            total_income = 0
            total_expense = 0
            income_details = []
            expense_details = []
            
            # 處理兩個數據源
            for data_path in self.data_paths:
                if not os.path.exists(data_path):
                    continue
                    
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 計算總收支
                for month, month_data in data.items():
                    for entry in month_data:
                        if len(entry) > 2:
                            user = self.resolve_name(entry[2])
                            owner = self.resolve_name(entry[3]) if len(entry) > 3 else None
                            
                            # 處理收入（使用人）
                            if user == selected_person:
                                try:
                                    amount = float(entry[1])
                                    total_expense += amount
                                    market = self.resolve_name(entry[0])
                                    expense_details.append(f"{month} - {market}: NT$ {amount:,}")
                                except (ValueError, IndexError):
                                    pass
                            
                            # 處理支出（所有人）
                            elif owner == selected_person:
                                try:
                                    amount = float(entry[1])
                                    total_income += amount
                                    market = self.resolve_name(entry[0])
                                    income_details.append(f"{month} - {market}: NT$ {amount:,}")
                                except (ValueError, IndexError):
                                    pass
            
            # 顯示結果
            summary_text = f"{selected_person} 的總收支:\n"
            summary_text += f"收入: NT$ {total_income:,}\n"
            summary_text += f"支出: NT$ {total_expense:,}\n"
            summary_text += f"淨收入: NT$ {total_income - total_expense:,}"
            
            self.total_income = total_income
            self.total_expense = total_expense
            
            # 顯示明細
            self.income_label.setText("\n".join(income_details) if income_details else "無收入記錄")
            self.expense_label.setText("\n".join(expense_details) if expense_details else "無支出記錄")
            
            # 更新總收支顯示
            if hasattr(self, 'summary_label'):
                self.summary_label.deleteLater()
                
            self.summary_label = QLabel(summary_text)
            self.content_layout.addWidget(self.summary_label, 2, 0, 1, 2)
            
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"計算收支時發生錯誤: {str(e)}")
            
    def print_summary(self):
        """列印總結"""
        selected_person = self.person_combo.currentText()
        if not selected_person:
            QMessageBox.warning(self, "警告", "請先選擇人員並計算收支")
            return
            
        try:
            full_text = f"<h1>{selected_person} 的總收支</h1><br>"
            full_text += f"<p>收入: NT$ {self.total_income:,}</p>"
            full_text += f"<p>支出: NT$ {self.total_expense:,}</p>"
            full_text += f"<p>淨收入: NT$ {self.total_income - self.total_expense:,}</p><br>"
            
            full_text += "<h2>收支明細:</h2>"
            full_text += "<table width='100%'><tr>"
            full_text += "<td width='50%' valign='top'><h3>收入明細:</h3>"
            full_text += "<p>" + self.income_label.text().replace("\n", "<br>") + "</p></td>"
            full_text += "<td width='50%' valign='top'><h3>支出明細:</h3>"
            full_text += "<p>" + self.expense_label.text().replace("\n", "<br>") + "</p></td>"
            full_text += "</tr></table>"
            
            doc = QTextDocument()
            doc.setHtml(full_text)
                    
            printer = QPrinter()
            print_dialog = QPrintDialog(printer, self)
            if print_dialog.exec() == QPrintDialog.Accepted:
                doc.print_(printer)
                
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"列印時發生錯誤: {str(e)}")
