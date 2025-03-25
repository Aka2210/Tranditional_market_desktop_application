from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QCalendarWidget, QScrollArea, QGridLayout, QFrame, QSizePolicy
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont
from lib.func import load_json

class DateViewer(QWidget):
    def __init__(self, data_path, parent=None):
        super().__init__(parent)
        self.data_path = data_path
        self.data = load_json(data_path)
        self.initUI()
        self.resizeEvent = self.onResize

    def initUI(self):
        self.setWindowTitle("日期資料檢視")
        self.setMinimumSize(1000, 600)
        self.resize(1200, 800)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Calendar selection (smaller size)
        calendar_container = QWidget()
        calendar_layout = QVBoxLayout(calendar_container)
        calendar_layout.setContentsMargins(0, 0, 0, 0)
        
        self.calendar = QCalendarWidget()
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate(2023, 1, 1))
        self.calendar.setMaximumDate(QDate(2030, 12, 31))
        self.calendar.setFixedSize(400, 300)
        self.calendar.clicked.connect(self.loadData)
        
        calendar_layout.addWidget(self.calendar, 0, Qt.AlignCenter)
        main_layout.addWidget(calendar_container)
        
        # Single scroll area for both columns
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.data_container = QWidget()
        self.grid_layout = QGridLayout(self.data_container)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        
        # Set initial column widths and spacing
        self.updateColumnWidths()
        self.grid_layout.setHorizontalSpacing(10)
        self.grid_layout.setVerticalSpacing(5)
        
        # Set size policies
        self.data_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll.setWidget(self.data_container)
        main_layout.addWidget(self.scroll)
        
        # Load initial data
        self.loadData()

    def updateColumnWidths(self):
        width = self.width()
        self.column_width = max(100, width // 12)
        
        for i in range(5):  # 5 columns per side
            self.grid_layout.setColumnMinimumWidth(i, self.column_width)
            self.grid_layout.setColumnMinimumWidth(i + 5, self.column_width)
            self.grid_layout.setColumnStretch(i, 1)
            self.grid_layout.setColumnStretch(i + 5, 1)

    def onResize(self, event):
        self.updateColumnWidths()
        event.accept()

    def loadData(self):
        # Clear existing data
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
            
        date_str = self.calendar.selectedDate().toString("yyyy-MM-dd")
        if date_str not in self.data:
            return
            
        # Add headers
        headers = ["市場", "租金", "所有人", "使用人", "備註"]
        header_font = QFont("Arial", 10, QFont.Bold)
        
        # Add column dividers and headers
        for i, header in enumerate(headers):
            # Left column header
            left_header = QLabel(header)
            left_header.setFont(header_font)
            left_header.setAlignment(Qt.AlignCenter)
            self.grid_layout.addWidget(left_header, 0, i)
            
            # Right column header
            right_header = QLabel(header)
            right_header.setFont(header_font)
            right_header.setAlignment(Qt.AlignCenter)
            self.grid_layout.addWidget(right_header, 0, i + 5)
            
            # Add vertical divider
            if i == 4:
                divider = QFrame()
                divider.setFrameShape(QFrame.VLine)
                divider.setFrameShadow(QFrame.Sunken)
                self.grid_layout.addWidget(divider, 0, 5, -1, 1)
            
        # Add data with styling
        row_data = self.data[date_str]
        half_length = len(row_data) // 2
        
        # Left column data
        for row_idx in range(half_length):
            row = row_data[row_idx]
            for col_idx, value in enumerate(row):
                label = QLabel(str(value))
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("padding: 5px;")
                
                # Alternate row background
                if row_idx % 2 == 0:
                    label.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
                
                self.grid_layout.addWidget(label, row_idx + 1, col_idx, Qt.AlignCenter)
        
        # Right column data
        for row_idx in range(half_length, len(row_data)):
            row = row_data[row_idx]
            for col_idx, value in enumerate(row):
                label = QLabel(str(value))
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("padding: 5px;")
                
                # Alternate row background
                if row_idx % 2 == 0:
                    label.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
                
                self.grid_layout.addWidget(label, row_idx - half_length + 1, col_idx + 5, Qt.AlignCenter)
