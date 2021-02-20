# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 425)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_calls = QtWidgets.QAction(MainWindow)
        self.action_calls.setObjectName("action_calls")
        self.action_income = QtWidgets.QAction(MainWindow)
        self.action_income.setObjectName("action_income")
        self.action_online = QtWidgets.QAction(MainWindow)
        self.action_online.setObjectName("action_online")
        self.toolBar.addAction(self.action_calls)
        self.toolBar.addAction(self.action_income)
        self.toolBar.addAction(self.action_online)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_calls.setText(_translate("MainWindow", "呼入统计"))
        self.action_income.setText(_translate("MainWindow", "收入统计"))
        self.action_online.setText(_translate("MainWindow", "在线咨询统计"))

