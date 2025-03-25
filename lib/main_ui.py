# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCalendarWidget, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStackedWidget, QStatusBar, QVBoxLayout, QWidget)
from resources import main_icon

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 800)
        self.binding = QAction(MainWindow)
        self.binding.setObjectName(u"binding")
        self.bindingCode = QAction(MainWindow)
        self.bindingCode.setObjectName(u"bindingCode")
        self.fixedRent = QAction(MainWindow)
        self.fixedRent.setObjectName(u"fixedRent")
        self.moneyCalculate = QAction(MainWindow)
        self.moneyCalculate.setObjectName(u"moneyCalculate")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.calendarWidget = QCalendarWidget(self.centralwidget)
        self.calendarWidget.setObjectName(u"calendarWidget")

        self.verticalLayout.addWidget(self.calendarWidget, 0, Qt.AlignmentFlag.AlignTop)

        self.stackedWidget_2 = QStackedWidget(self.centralwidget)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.verticalLayout_3 = QVBoxLayout(self.page_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.top_label = QWidget(self.page_5)
        self.top_label.setObjectName(u"top_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top_label.sizePolicy().hasHeightForWidth())
        self.top_label.setSizePolicy(sizePolicy)
        self.horizontalLayout_5 = QHBoxLayout(self.top_label)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.market = QLabel(self.top_label)
        self.market.setObjectName(u"market")

        self.horizontalLayout_5.addWidget(self.market, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.rent = QLabel(self.top_label)
        self.rent.setObjectName(u"rent")

        self.horizontalLayout_5.addWidget(self.rent, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.owner = QLabel(self.top_label)
        self.owner.setObjectName(u"owner")

        self.horizontalLayout_5.addWidget(self.owner, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.user = QLabel(self.top_label)
        self.user.setObjectName(u"user")

        self.horizontalLayout_5.addWidget(self.user, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.note = QLabel(self.top_label)
        self.note.setObjectName(u"note")

        self.horizontalLayout_5.addWidget(self.note, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.verticalLayout_3.addWidget(self.top_label, 0, Qt.AlignmentFlag.AlignTop)

        self.scrollArea_2 = QScrollArea(self.page_5)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy1)
        self.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea_2.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 762, 641))
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_3.addWidget(self.scrollArea_2)

        self.addColumn = QPushButton(self.page_5)
        self.addColumn.setObjectName(u"addColumn")

        self.verticalLayout_3.addWidget(self.addColumn)

        self.stackedWidget_2.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.stackedWidget_2.addWidget(self.page_6)

        self.verticalLayout.addWidget(self.stackedWidget_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 27))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.bindingCode)
        self.menu.addAction(self.fixedRent)
        self.menu.addAction(self.moneyCalculate)

        self.retranslateUi(MainWindow)

        self.stackedWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.binding.setText(QCoreApplication.translate("MainWindow", u"\u5217\u5370\u6b64\u9801", None))
        self.bindingCode.setText(QCoreApplication.translate("MainWindow", u"\u4ee3\u865f\u8a2d\u7f6e", None))
        self.fixedRent.setText(QCoreApplication.translate("MainWindow", u"\u56fa\u5b9a\u4f4d\u79df\u4fee\u6539", None))
        self.moneyCalculate.setText(QCoreApplication.translate("MainWindow", u"\u91d1\u984d\u8a08\u7b97", None))
        self.market.setText(QCoreApplication.translate("MainWindow", u"\u5e02\u5834", None))
        self.rent.setText(QCoreApplication.translate("MainWindow", u"\u79df\u91d1", None))
        self.owner.setText(QCoreApplication.translate("MainWindow", u"\u6240\u6709\u4eba", None))
        self.user.setText(QCoreApplication.translate("MainWindow", u"\u4f7f\u7528\u4eba", None))
        self.note.setText(QCoreApplication.translate("MainWindow", u"\u5099\u8a3b", None))
        self.addColumn.setText(QCoreApplication.translate("MainWindow", u"\u589e\u52a0\u6b04\u4f4d", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u8a2d\u5b9a", None))
    # retranslateUi

