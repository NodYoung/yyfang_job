# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\income_widget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_IncomeWidget(object):
    def setupUi(self, IncomeWidget):
        IncomeWidget.setObjectName("IncomeWidget")
        IncomeWidget.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(IncomeWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(IncomeWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_workorder_filepath = QtWidgets.QLineEdit(IncomeWidget)
        self.lineEdit_workorder_filepath.setObjectName("lineEdit_workorder_filepath")
        self.horizontalLayout.addWidget(self.lineEdit_workorder_filepath)
        self.pushButton_workorder_browse = QtWidgets.QPushButton(IncomeWidget)
        self.pushButton_workorder_browse.setObjectName("pushButton_workorder_browse")
        self.horizontalLayout.addWidget(self.pushButton_workorder_browse)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(IncomeWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_session_filepath = QtWidgets.QLineEdit(IncomeWidget)
        self.lineEdit_session_filepath.setObjectName("lineEdit_session_filepath")
        self.horizontalLayout_2.addWidget(self.lineEdit_session_filepath)
        self.pushButton_session_browse = QtWidgets.QPushButton(IncomeWidget)
        self.pushButton_session_browse.setObjectName("pushButton_session_browse")
        self.horizontalLayout_2.addWidget(self.pushButton_session_browse)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(IncomeWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_fee_filepath = QtWidgets.QLineEdit(IncomeWidget)
        self.lineEdit_fee_filepath.setObjectName("lineEdit_fee_filepath")
        self.horizontalLayout_3.addWidget(self.lineEdit_fee_filepath)
        self.pushButton_fee_browse = QtWidgets.QPushButton(IncomeWidget)
        self.pushButton_fee_browse.setObjectName("pushButton_fee_browse")
        self.horizontalLayout_3.addWidget(self.pushButton_fee_browse)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton_calc = QtWidgets.QPushButton(IncomeWidget)
        self.pushButton_calc.setObjectName("pushButton_calc")
        self.verticalLayout.addWidget(self.pushButton_calc)
        spacerItem = QtWidgets.QSpacerItem(20, 157, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(IncomeWidget)
        QtCore.QMetaObject.connectSlotsByName(IncomeWidget)

    def retranslateUi(self, IncomeWidget):
        _translate = QtCore.QCoreApplication.translate
        IncomeWidget.setWindowTitle(_translate("IncomeWidget", "Form"))
        self.label.setText(_translate("IncomeWidget", "工单报表："))
        self.pushButton_workorder_browse.setText(_translate("IncomeWidget", "..."))
        self.label_2.setText(_translate("IncomeWidget", "会话记录报表："))
        self.pushButton_session_browse.setText(_translate("IncomeWidget", "..."))
        self.label_3.setText(_translate("IncomeWidget", "学费报表："))
        self.pushButton_fee_browse.setText(_translate("IncomeWidget", "..."))
        self.pushButton_calc.setText(_translate("IncomeWidget", "计算结果"))

