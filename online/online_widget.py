from .ui_online_widget import Ui_OnlineWidget
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import numpy as np
import pandas as pd
import time
import logging

class OnlineWidget(QWidget):
  def __init__(self):
    super().__init__()
    self.ui = Ui_OnlineWidget()
    self.ui.setupUi(self)
    self.ui.lineEdit_filepath.setText('D:/yyfang/210216/data/session_record_sample/receptionRecord_20210215-20210217_c4856183-1f05-4a30-8d2d-80cc3c63a501.xlsx')

  @pyqtSlot()
  def on_pushButton_file_browse_clicked(self):
    filepath, _ = QFileDialog.getOpenFileName(self, 'Open file', self.ui.lineEdit_filepath.text(), 'Excel (*.xls *.xlsx)')
    if filepath:
      self.ui.lineEdit_filepath.setText(filepath)
  
  @pyqtSlot()
  def on_pushButton_calc_clicked(self):
    session_data_path = self.ui.lineEdit_filepath.text()
    try:
      session_data = pd.read_excel(session_data_path, usecols=['会话建立时间'])
      session_data['会话建立时间'] = pd.to_datetime(session_data['会话建立时间'],format='%Y-%m-%d %H:%M:%S')   # 更改时间为统一格式
      self.calc_hour_info(session_data, session_data_path)
    except Exception as e:
      logging.exception(e)
      QMessageBox.warning(self, 'warning', '计算出错，可能原因：\n \
                                            1.文件已经在WPS中打开，请先在WPS中关闭该文档；')
      return
    QMessageBox.information(self, 'info', '计算完成！')

  def calc_hour_info(self, session_data, session_data_path):
    # 统计呼叫时间
    session_data['hour'] = session_data['会话建立时间'].apply(lambda x: time.strptime(x.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').tm_hour*2+time.strptime(x.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').tm_min//30)
    time_frequency = session_data['hour'].value_counts().sort_index()
    time_frequency = time_frequency.rename('呼入')
    time_frequency.index = time_frequency.index/2
    hour_info = pd.concat([time_frequency], axis =1)
    hour_info = hour_info.fillna(0)
    hour_info['时间'] = hour_info.index
    hour_info['时间'] = hour_info['时间'].apply(lambda x: '%d:%02d-%d:%02d' % (x//1, x%1*60, (x+0.5)//1, (x+0.5)%1*60))
    hour_info = hour_info[['时间', '呼入']]
    # time_frequency.index = time_frequency.index/2
    # time_series = time_frequency.index
    # time_series = time_series.apply(lambda x: '%d:%02d-%d:%02d' % (x//1, x%1*60, (x+0.5)//1, (x+0.5)%1*60))
    # time_series = time_series.rename('时间')
    with pd.ExcelWriter(session_data_path, engine='openpyxl', mode='a') as writer:  
      hour_info.to_excel(writer, sheet_name='时间段统计', index=False)
