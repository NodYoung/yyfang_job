import logging, os, datetime
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from .ui_mainwindow import Ui_MainWindow
from calls import CallsWidget
from income import IncomeWidget
from online import OnlineWidget

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.calls_widget = None
    self.income_widget = None
    self.online_widget = None

  @pyqtSlot()
  def on_action_calls_triggered(self):
    if self.calls_widget is None:
        self.calls_widget = CallsWidget()
    self.calls_widget.show()

  @pyqtSlot()
  def on_action_income_triggered(self):
    if self.income_widget is None:
        self.income_widget = IncomeWidget()
    self.income_widget.show()

  @pyqtSlot()
  def on_action_online_triggered(self):
    if self.online_widget is None:
        self.online_widget = OnlineWidget()
    self.online_widget.show()