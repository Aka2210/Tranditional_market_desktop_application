from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QSpacerItem, QSizePolicy, QFileDialog,
    QComboBox, QMessageBox
)
from PySide6.QtCore import Qt, QDate, QPoint
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QPainter, QPageSize, QPageLayout, QTextDocument
from datetime import datetime
import json
import os
from collections import defaultdict

class RentSummaryInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("輸入報表條件")
        self.resize(300, 200)

        layout = QVBoxLayout(self)

        # 掃描所有名稱以建立選單
        names_set = set()
        for path in ["resources/jsonData/mainData.json", "resources/jsonData/fixedRentData.json"]:
            if os.path.exists(path):
                try:
                    with open(path, encoding="utf-8") as f:
                        data = json.load(f)
                        for entries in data.values():
                            for entry in entries:
                                if isinstance(entry, list) and len(entry) >= 4:
                                    if entry[2]:  # 使用人
                                        names_set.add(entry[2])
                                    if entry[3]:  # 所有人
                                        names_set.add(entry[3])
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error reading {path}: {e}")
            else:
                print(f"File not found: {path}")

        # 加入代號綁定名稱
        bindings_path = "resources/jsonData/name_bindings.json"
        if os.path.exists(bindings_path):
            with open(bindings_path, encoding="utf-8") as f:
                bindings = json.load(f)
                names_set.update(bindings.keys())
                names_set.update(bindings.values())

        sorted_names = sorted(names_set)

        # 所有人
        self.owner_input = QComboBox()
        self.owner_input.setEditable(True)
        self.owner_input.addItems(sorted_names)
        self.owner_input.setInsertPolicy(QComboBox.InsertAtTop)
        layout.addWidget(QLabel("公司所有人："))
        layout.addWidget(self.owner_input)

        # 使用人
        self.user_input = QComboBox()
        self.user_input.setEditable(True)
        self.user_input.addItems(sorted_names)
        self.user_input.setInsertPolicy(QComboBox.InsertAtTop)
        layout.addWidget(QLabel("使用人："))
        layout.addWidget(self.user_input)

        # 年、月
        self.year_input = QComboBox()
        self.year_input.addItems([str(year) for year in range(2020, 2031)])
        layout.addWidget(QLabel("年份："))
        layout.addWidget(self.year_input)

        self.month_input = QComboBox()
        self.month_input.addItems([str(month) for month in range(1, 13)])
        layout.addWidget(QLabel("月份："))
        layout.addWidget(self.month_input)

        # 服務費用
        self.service_fee_input = QLineEdit()
        self.service_fee_input.setPlaceholderText("輸入服務費用")
        layout.addWidget(QLabel("服務費用："))
        layout.addWidget(self.service_fee_input)

        # 確定按鈕
        self.confirm_button = QPushButton("確定")
        self.confirm_button.clicked.connect(self.check_and_accept)
        layout.addWidget(self.confirm_button)

    def check_and_accept(self):
        owner = self.owner_input.currentText().strip()
        user = self.user_input.currentText().strip()
        if not owner or not user:
            QMessageBox.warning(self, "輸入錯誤", "所有人與使用人不可為空白")
            return
        self.accept()

    def get_inputs(self):
        return (
            self.owner_input.currentText().strip(),
            self.user_input.currentText().strip(),
            self.year_input.currentText(),
            self.month_input.currentText(),
            self.service_fee_input.text().strip()
        )

class RentSummaryPreview(QDialog):
    def __init__(self, owner: str, user: str, year: str, month: str, service_fee: str, parent=None):
        # 新增服務費用處理
        try:
            self.service_fee = int(service_fee) if service_fee else 0
        except ValueError:
            self.service_fee = 0
        super().__init__(parent)
        main_path = os.path.join("resources", "jsonData", "mainData.json")
        fixed_path = os.path.join("resources", "jsonData", "fixedRentData.json")
        name_bindings_path = os.path.join("resources", "jsonData", "name_bindings.json")
        market_bindings_path = os.path.join("resources", "jsonData", "market_bindings.json")

        with open(main_path, encoding="utf-8") as f:
            main_data = json.load(f)

        with open(fixed_path, encoding="utf-8") as f:
            fixed_data = json.load(f)

        name_bindings = {}
        if os.path.exists(name_bindings_path):
            with open(name_bindings_path, encoding="utf-8") as f:
                name_bindings = json.load(f)

        market_bindings = {}
        if os.path.exists(market_bindings_path):
            with open(market_bindings_path, encoding="utf-8") as f:
                market_bindings = json.load(f)

        self.setWindowTitle("租金應收付明細表 預覽")
        self.resize(1200, 850)

        self.layout = QVBoxLayout(self)

        self.title_label = QLabel(f"<h1>{name_bindings.get(owner, owner)} 租金應收付明細表</h1>")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.meta_layout = QHBoxLayout()
        self.meta_layout.setSpacing(50)
        self.meta_layout.addWidget(QLabel(f"客戶名稱：{name_bindings.get(user, user)}"))

        start_date = f"{year}/{month.zfill(2)}/01"
        qdate_start = QDate(int(year), int(month), 1)
        qdate_end = qdate_start.addMonths(1).addDays(-1)
        end_date = qdate_end.toString("yyyy/MM/dd")
        self.meta_layout.addWidget(QLabel(f"起始日期：{start_date} 到 {end_date}"))

        today = datetime.today().strftime("%Y/%m/%d")
        self.meta_layout.addWidget(QLabel(f"列印日期：{today}"))
        self.layout.addLayout(self.meta_layout)

        def match_name(name1, name2):
            resolved1 = name_bindings.get(name1, name1)
            resolved2 = name_bindings.get(name2, name2)
            return resolved1 == resolved2

        def resolve_market(market):
            return market_bindings.get(market, market)

        combined_data = defaultdict(list)

        for date, entries in main_data.items():
            combined_data[date].extend(entries)
        for date, entries in fixed_data.items():
            combined_data[date].extend(entries)

        owner_total = 0
        user_total = 0
        user_row = 0
        owner_row = 0

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["承租日期", "星期", "租位名稱", "租金", "承租日期", "星期", "租位名稱", "租金"])
        self.table.setRowCount(0)
        self.table.setStyleSheet("QTableWidget { font-size: 18px; padding: 12px; }")

        # 按日期排序處理資料
        sorted_dates = sorted(
            combined_data.keys(),
            key=lambda x: datetime.strptime(x, "%Y-%m-%d").toordinal()
        )
        
        for date in sorted_dates:
            entry_list = combined_data[date]
            if not entry_list or not isinstance(entry_list, list):
                continue
            entry_year, entry_month = date.split("-")[0], date.split("-")[1]
            if entry_year == year and entry_month == month.zfill(2):
                qdate = QDate.fromString(date, "yyyy-MM-dd")
                weekday_zh = "日一二三四五六"[qdate.dayOfWeek() % 7] if qdate.isValid() else ""
                for entry in entry_list:
                    if not isinstance(entry, list) or len(entry) < 4:
                        continue
                    flat_data = []
                    market, rent, entry_owner, entry_user = entry[0], entry[1], entry[2], entry[3]
                    if market == "" or rent == "" or entry_owner == "" or entry_user == "":
                        continue
                    if (
                        (entry_user == user)
                        or (entry_owner == user)
                        or (match_name(entry_user, user))
                        or (match_name(entry_owner, user))
                    ):
                        resolved_market = resolve_market(market)
                        flat_data.extend([date.replace("-", "/"), weekday_zh, resolved_market, rent])
                        rent_value = int(rent.replace(",", ""))
                        if match_name(entry_user, user):
                            owner_total += rent_value
                            user_total -= rent_value
                            if self.table.rowCount() <= user_row:
                                self.table.insertRow(self.table.rowCount())
                            for i in range(4):
                                item = QTableWidgetItem(flat_data[i])
                                item.setTextAlignment(Qt.AlignCenter)
                                self.table.setItem(user_row, i, item)
                            user_row += 1
                        elif match_name(entry_owner, user):
                            user_total += rent_value
                            owner_total -= rent_value
                            if self.table.rowCount() <= owner_row:
                                self.table.insertRow(self.table.rowCount())
                            for i in range(4, 8):
                                item = QTableWidgetItem(flat_data[i - 4])
                                item.setTextAlignment(Qt.AlignCenter)
                                self.table.setItem(owner_row, i, item)
                            owner_row += 1

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.table)

        self.diff_label = QLabel()
        self.diff_label.setAlignment(Qt.AlignRight)
        self.diff_label.setStyleSheet("font-size: 18px; padding: 12px;")
        if user_total > 0:
            self.diff_label.setText(f"{user}需額外支付服務費：{service_fee} 元\n因此{user}需收到：{user_total - int(service_fee)} 元, {owner}需支付：{user_total - int(service_fee)} 元")
        elif owner_total > 0:
            self.diff_label.setText(f"{user}需額外支付服務費：{service_fee} 元\n因此{name_bindings.get(owner, owner)}需收到：{owner_total + int(service_fee)} 元, {user}需支付：{owner_total + int(service_fee)} 元")
        self.layout.addWidget(self.diff_label)

        btn_layout = QHBoxLayout()
        self.print_btn = QPushButton("列印")
        self.print_btn.clicked.connect(self.handle_print)
        btn_layout.addStretch()
        btn_layout.addWidget(self.print_btn)
        self.layout.addLayout(btn_layout)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.close_btn = QPushButton("關閉")
        self.close_btn.clicked.connect(self.close)
        self.layout.addWidget(self.close_btn)

    def handle_print(self):
        self.print_btn.hide()
        self.close_btn.hide()

        # 取得資訊
        owner = self.title_label.text().replace("<h1>", "").replace("</h1>", "").strip()
        user = self.meta_layout.itemAt(0).widget().text().replace("客戶名稱：", "")
        date_range = self.meta_layout.itemAt(1).widget().text().replace("起始日期：", "")
        print_date = self.meta_layout.itemAt(2).widget().text().replace("列印日期：", "")
        diff_text = self.diff_label.text().replace("\n", "&nbsp;&nbsp;&nbsp;&nbsp;")

        # HTML 開頭
        html = f"""
        <div style="text-align:center; font-size:20pt; font-weight:bold; margin-bottom:10px;">
            {owner} 租金應收付明細表
        </div>

        <!-- 資訊欄 -->
        <div style="text-align:center; font-size:10pt; margin-bottom:20px;">
            <span><b>客戶名稱：</b>{user}</span>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <span><b>起始日期：</b>{date_range}</span>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <span><b>列印日期：</b>{print_date}</span>
        </div>

        <!-- 表格開始 -->
        <div style="text-align:center;">
        <table border='1' cellspacing='0' cellpadding='6'
            style='margin:auto; font-size:11pt; border-collapse:collapse; width:90%; text-align:center;'>
            <thead>
                <tr style='background-color:#f0f0f0;'>
        """

        # 加入欄位名稱
        for col in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(col).text()
            html += f"<th style='text-align:center;'>{header}</th>"

        html += "</tr></thead><tbody>"

        # 加入表格資料
        for row in range(self.table.rowCount()):
            html += "<tr>"
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                text = item.text() if item else ""
                html += f"<td style='text-align:center;'>{text}</td>"
            html += "</tr>"

        html += "</tbody></table></div>"

        # 收付款說明（右下角）
        html += f"""
        <div style="width:90%; font-size:10pt; text-align:right; margin-top:30px; margin-left:auto; margin-right:auto;">
            {diff_text}
        </div>
        """

        # 建立文件列印
        document = QTextDocument()
        document.setHtml(html)

        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPageSize(QPageSize.A4))
        printer.setPageOrientation(QPageLayout.Portrait)

        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.Accepted:
            document.print_(printer)

        self.print_btn.show()
        self.close_btn.show()
