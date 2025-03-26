import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QCalendarWidget, QMessageBox, QCheckBox, QDateEdit, QListWidget
)
from PySide6.QtCore import Qt, QDate

class FixedRentEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("固定位租修改")
        self.resize(800, 600)
        self.data_path = "resources/jsonData/fixedRentData.json"
        self.data_dict = {}
        self.selected_dates = []

        self.main_layout = QVBoxLayout(self)

        # 資料輸入區
        self.input_widget = QWidget()
        input_layout = QHBoxLayout(self.input_widget)
        
        # 市場
        market_widget = QWidget()
        market_layout = QVBoxLayout(market_widget)
        market_layout.addWidget(QLabel("市場:"))
        self.market_input = QLineEdit()
        market_layout.addWidget(self.market_input)
        input_layout.addWidget(market_widget)
        
        # 租金
        rent_widget = QWidget()
        rent_layout = QVBoxLayout(rent_widget)
        rent_layout.addWidget(QLabel("租金:"))
        self.rent_input = QLineEdit()
        rent_layout.addWidget(self.rent_input)
        input_layout.addWidget(rent_widget)
        
        # 所有人
        owner_widget = QWidget()
        owner_layout = QVBoxLayout(owner_widget)
        owner_layout.addWidget(QLabel("所有人:"))
        self.owner_input = QLineEdit()
        owner_layout.addWidget(self.owner_input)
        input_layout.addWidget(owner_widget)
        
        # 使用人
        user_widget = QWidget()
        user_layout = QVBoxLayout(user_widget)
        user_layout.addWidget(QLabel("使用人:"))
        self.user_input = QLineEdit()
        user_layout.addWidget(self.user_input)
        input_layout.addWidget(user_widget)
        
        # 備註
        note_widget = QWidget()
        note_layout = QVBoxLayout(note_widget)
        note_layout.addWidget(QLabel("備註:"))
        self.note_input = QLineEdit()
        note_layout.addWidget(self.note_input)
        input_layout.addWidget(note_widget)
        
        self.main_layout.addWidget(self.input_widget)

        # 每週重複設定區
        repeat_widget = QWidget()
        repeat_layout = QVBoxLayout(repeat_widget)
        
        # 每週重複設定
        self.week_days = []
        week_days_widget = QWidget()
        week_days_layout = QHBoxLayout(week_days_widget)
        for day in ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]:
            cb = QCheckBox(day)
            self.week_days.append(cb)
            week_days_layout.addWidget(cb)
        repeat_layout.addWidget(QLabel("每週重複:"))
        repeat_layout.addWidget(week_days_widget)
        
        # 日期範圍
        date_range_widget = QWidget()
        date_range_layout = QHBoxLayout(date_range_widget)
        date_range_layout.addWidget(QLabel("日期範圍:"))
        self.start_date = QDateEdit(QDate.currentDate())
        self.end_date = QDateEdit(QDate.currentDate().addMonths(1))
        date_range_layout.addWidget(self.start_date)
        date_range_layout.addWidget(QLabel("至"))
        date_range_layout.addWidget(self.end_date)
        repeat_layout.addWidget(date_range_widget)
        
        # 應用按鈕
        self.apply_btn = QPushButton("應用日期設定")
        self.apply_btn.clicked.connect(self.applyDates)
        repeat_layout.addWidget(self.apply_btn)
        
        self.main_layout.addWidget(repeat_widget)

        # 固定位租列表
        self.fixed_rent_list = QListWidget()
        self.main_layout.addWidget(QLabel("已設定的固定位租:"))
        self.main_layout.addWidget(self.fixed_rent_list)
        
        # 刪除按鈕
        self.delete_btn = QPushButton("刪除選中項目")
        self.delete_btn.clicked.connect(self.deleteSelectedFixedRent)
        self.main_layout.addWidget(self.delete_btn)
        
        # 控制列（關閉按鈕）
        self.button_row = QWidget()
        btn_layout = QHBoxLayout(self.button_row)
        self.close_button = QPushButton("關閉")
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_button)
        self.main_layout.addWidget(self.button_row)
        
        # 功能綁定
        self.close_button.clicked.connect(self.close)
        
        # 初始載入資料
        self.loadFixedRentData()

    def loadFixedRentData(self):
        """載入已存的固定位租資料"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.data_dict = json.load(f)
            self.updateFixedRentList()
        except FileNotFoundError:
            self.data_dict = {}
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"無法載入資料: {str(e)}")

    def updateFixedRentList(self):
        """更新固定位租列表（按日期排序）"""
        self.fixed_rent_list.clear()
        self.entry_map = {}  # 用於映射列表項文本到數據索引
        
        # 按日期排序
        sorted_dates = sorted(self.data_dict.items(), key=lambda x: QDate.fromString(x[0], "yyyy-MM-dd"))
        
        for date, entries in sorted_dates:
            for i, entry in enumerate(entries):
                item_text = f"{date}: 市場: {entry[0]}, 租金: {entry[1]}元, 所有人: {entry[2]}, 使用人: {entry[3]}, 備註: {entry[4]}"
                self.fixed_rent_list.addItem(item_text)
                # 使用文本作為映射鍵
                self.entry_map[item_text] = (date, i)

    def applyDates(self):
        """應用每週重複日期設定"""
        if len(self.market_input.text()) == 0:
            QMessageBox.warning(self, "錯誤", "請填入市場名稱")
            return
            
        try:
            float(self.rent_input.text())
        except ValueError:
            QMessageBox.warning(self, "錯誤", "租金必須是數字")
            return

        data = [self.market_input.text(),
                self.rent_input.text(),
                self.owner_input.text(),
                self.user_input.text(),
                self.note_input.text()]
        
        # 處理每週重複日期
        start_date = self.start_date.date()
        end_date = self.end_date.date()
        current_date = start_date
        
        while current_date <= end_date:
            for i, cb in enumerate(self.week_days):
                if cb.isChecked() and current_date.dayOfWeek() == i + 1:
                    self.saveDataForDate(current_date, data)
            current_date = current_date.addDays(1)
        
        QMessageBox.information(self, "成功", "已成功設定每週重複日期")
        
    def saveDataForDate(self, date, data):
        """將資料保存到指定日期並更新列表"""
        date_str = date.toString("yyyy-MM-dd")
        if date_str not in self.data_dict:
            self.data_dict[date_str] = []
        self.data_dict[date_str].append(data)
        self.updateFixedRentList()
        
    def deleteSelectedFixedRent(self):
        """刪除選中的固定位租"""
        selected_item = self.fixed_rent_list.currentItem()
        if selected_item:
            item_text = selected_item.text()
            if item_text in self.entry_map:
                date_str, entry_index = self.entry_map[item_text]
            
            # 從數據中刪除特定條目
            if date_str in self.data_dict and entry_index < len(self.data_dict[date_str]):
                del self.data_dict[date_str][entry_index]
                
                # 如果該日期沒有其他條目，刪除整個日期
                if not self.data_dict[date_str]:
                    del self.data_dict[date_str]
            
            self.updateFixedRentList()
        
    def closeEvent(self, event):
        try:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(self.data_dict, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"保存數據失敗: {str(e)}")
        event.accept()
