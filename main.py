#!/usr/bin/env python
# -*-coding:utf-8-*-
import sys
import logging
from PyQt5.QtWidgets import QApplication
from mainwindow.mainwindow import MainWindow


if __name__ == '__main__':
  logging.basicConfig(format="%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s", level=logging.INFO)
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())