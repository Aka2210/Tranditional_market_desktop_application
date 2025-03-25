import json
import os
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QComboBox, QPushButton, QMessageBox)
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QTextDocument
from lib.bindingCode import NameBindingDialog

class PersonSummaryDialog(QDialog):
    def __init__(self, data_path, parent=None):
        super().__init__(parent)
        self.data_path = data_path
        self.setWindowTitle("個人收支總結")
        self.resize(400, 300)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # 選擇人員
        self.person_combo = QComboBox()
        self.load_persons()
        layout.addWidget(QLabel("選擇人員:"))
        layout.addWidget(self.person_combo)
        
        # 顯示結果
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)
        
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
                    
            persons = set()
            
            # 從主數據加載出現過的所有人
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for month_data in data.values():
                        for entry in month_data:
                            if len(entry) > 2:  # 確保有使用人/所有人字段
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
        """計算選定人員的總收支"""
        selected_person = self.person_combo.currentText()
        if not selected_person:
            return
            
        try:
            # 加載主數據
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            total_income = 0
            total_expense = 0
            
            # 計算總收支（考慮綁定）
            for month_data in data.values():
                for entry in month_data:
                    if len(entry) > 2:  # 確保有使用人/所有人字段
                        # 解析使用人和所有人
                        user = entry[2]
                        owner = entry[3] if len(entry) > 3 else None
                        
                        # 檢查選定的實際用戶是誰
                        if self.resolve_name(user) == selected_person:  # 使用人
                            try:
                                total_income += float(entry[1])  # 租金收入
                            except (ValueError, IndexError):
                                pass
                        if owner and self.resolve_name(owner) == selected_person:  # 所有人
                            try:
                                total_expense += float(entry[1])  # 租金支出
                            except (ValueError, IndexError):
                                pass
                                
            # 收集明細
            income_details = []
            expense_details = []
            
            for month, month_data in data.items():
                for entry in month_data:
                    if len(entry) > 2:  # 確保有使用人/所有人字段
                        # 解析使用人和所有人
                        user = self.resolve_name(entry[2])
                        owner = self.resolve_name(entry[3]) if len(entry) > 3 else None
                        
                        if user == selected_person:  # 使用人
                            try:
                                amount = float(entry[1])
                                market = self.resolve_name(entry[0])  # 解析市場名稱
                                income_details.append(f"{month} - {market}: NT$ {amount:,}")
                            except (ValueError, IndexError):
                                pass
                        if owner == selected_person:  # 所有人
                            try:
                                amount = float(entry[1])
                                market = self.resolve_name(entry[0])  # 解析市場名稱
                                expense_details.append(f"{month} - {market}: NT$ {amount:,}")
                            except (ValueError, IndexError):
                                pass
                                
            # 顯示結果
            result_text = f"{selected_person} 的總收支:\n"
            result_text += f"收入: NT$ {total_income:,}\n"
            result_text += f"支出: NT$ {total_expense:,}\n"
            result_text += f"淨收入: NT$ {total_income - total_expense:,}\n\n"
            
            result_text += "收入明細:\n"
            result_text += "\n".join(income_details) if income_details else "無收入記錄\n"
            result_text += "\n\n支出明細:\n"
            result_text += "\n".join(expense_details) if expense_details else "無支出記錄"
            
            self.result_label.setText(result_text)
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"計算收支時發生錯誤: {str(e)}")
            
    def print_summary(self):
        """列印總結"""
        if not self.result_label.text():
            QMessageBox.warning(self, "警告", "請先計算收支")
            return
            
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec() == QPrintDialog.Accepted:
            doc = QTextDocument()
            doc.setPlainText(self.result_label.text())
            doc.print_(printer)
