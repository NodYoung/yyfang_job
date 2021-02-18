# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\calls_widget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CallsWidget(object):
    def setupUi(self, CallsWidget):
        CallsWidget.setObjectName("CallsWidget")
        CallsWidget.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(CallsWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(CallsWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_filepath = QtWidgets.QLineEdit(CallsWidget)
        self.lineEdit_filepath.setObjectName("lineEdit_filepath")
        self.horizontalLayout.addWidget(self.lineEdit_filepath)
        self.pushButton_file_browse = QtWidgets.QPushButton(CallsWidget)
        self.pushButton_file_browse.setObjectName("pushButton_file_browse")
        self.horizontalLayout.addWidget(self.pushButton_file_browse)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton_calc = QtWidgets.QPushButton(CallsWidget)
        self.pushButton_calc.setObjectName("pushButton_calc")
        self.verticalLayout.addWidget(self.pushButton_calc)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 217, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(CallsWidget)
        QtCore.QMetaObject.connectSlotsByName(CallsWidget)

    def retranslateUi(self, CallsWidget):
        _translate = QtCore.QCoreApplication.translate
        CallsWidget.setWindowTitle(_translate("CallsWidget", "Form"))
        self.label.setText(_translate("CallsWidget", "呼入量报表："))
        self.pushButton_file_browse.setText(_translate("CallsWidget", "..."))
        self.pushButton_calc.setText(_translate("CallsWidget", "计算结果"))

