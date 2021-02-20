# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\online_widget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OnlineWidget(object):
    def setupUi(self, OnlineWidget):
        OnlineWidget.setObjectName("OnlineWidget")
        OnlineWidget.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(OnlineWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(OnlineWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_filepath = QtWidgets.QLineEdit(OnlineWidget)
        self.lineEdit_filepath.setObjectName("lineEdit_filepath")
        self.horizontalLayout.addWidget(self.lineEdit_filepath)
        self.pushButton_file_browse = QtWidgets.QPushButton(OnlineWidget)
        self.pushButton_file_browse.setObjectName("pushButton_file_browse")
        self.horizontalLayout.addWidget(self.pushButton_file_browse)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton_calc = QtWidgets.QPushButton(OnlineWidget)
        self.pushButton_calc.setObjectName("pushButton_calc")
        self.verticalLayout.addWidget(self.pushButton_calc)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 217, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(OnlineWidget)
        QtCore.QMetaObject.connectSlotsByName(OnlineWidget)

    def retranslateUi(self, OnlineWidget):
        _translate = QtCore.QCoreApplication.translate
        OnlineWidget.setWindowTitle(_translate("OnlineWidget", "Form"))
        self.label.setText(_translate("OnlineWidget", "会话记录报表："))
        self.pushButton_file_browse.setText(_translate("OnlineWidget", "..."))
        self.pushButton_calc.setText(_translate("OnlineWidget", "计算结果"))

