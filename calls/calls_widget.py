from .ui_calls_widget import Ui_CallsWidget
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import numpy as np
import pandas as pd
import time
import logging

class CallsWidget(QWidget):
  def __init__(self):
    super().__init__()
    self.ui = Ui_CallsWidget()
    self.ui.setupUi(self)
    self.ui.lineEdit_filepath.setText('D:/yyfang/210216/data/calls_sample/呼入量.xlsx')
    

  @pyqtSlot()
  def on_pushButton_file_browse_clicked(self):
    filepath, _ = QFileDialog.getOpenFileName(self, 'Open file', self.ui.lineEdit_filepath.text(), 'Excel (*.xls *.xlsx)')
    if filepath:
      self.ui.lineEdit_filepath.setText(filepath)

  @pyqtSlot()
  def on_pushButton_calc_clicked(self):
    callin_data_path = self.ui.lineEdit_filepath.text()
    logging.info(callin_data_path)
    callin_data = pd.read_excel(callin_data_path)
    self.calc_call_time(callin_data, callin_data_path)
    self.calc_connection_status(callin_data, callin_data_path)
    self.calc_satisfaction(callin_data, callin_data_path)
    QMessageBox.information(self, 'info', '计算完成！')
    
  def calc_call_time(self, callin_data, callin_data_path):
    # 统计呼叫时间
    callin_data['hour'] = callin_data['呼叫时间'].apply(lambda x: time.strptime(x,'%Y-%m-%d %H:%M:%S').tm_hour*2+time.strptime(x,'%Y-%m-%d %H:%M:%S').tm_min//30)
    callin_time_frequency = callin_data['hour'].value_counts().sort_index()
    callin_time_frequency = callin_time_frequency.rename('all')
    callin_time_frequency.index = callin_time_frequency.index/2
    connection_time_frequency = callin_data.loc[callin_data['通话状态'] == '接通']['hour'].value_counts().sort_index()
    connection_time_frequency = connection_time_frequency.rename('connection')
    connection_time_frequency.index = connection_time_frequency.index/2
    missing_time_frequency = callin_data.loc[callin_data['通话状态'] == '未接通']['hour'].value_counts().sort_index()
    missing_time_frequency = missing_time_frequency.rename('missing')
    missing_time_frequency.index = missing_time_frequency.index/2
    time_frequency = pd.concat([callin_time_frequency, connection_time_frequency, missing_time_frequency], axis =1)
    time_frequency = time_frequency.fillna(0)
    time_frequency['time'] = time_frequency.index
    time_frequency['time'] = time_frequency['time'].apply(lambda x: '%d:%02d-%d:%02d' % (x//1, x%1*60, (x+0.5)//1, (x+0.5)%1*60))
    time_frequency = time_frequency[['time', 'all', 'connection', 'missing']]
    with pd.ExcelWriter(callin_data_path, engine='openpyxl', mode='a') as writer:  
      time_frequency.to_excel(writer, sheet_name='时间段统计', index=False)
      
  def calc_connection_status(self, callin_data, callin_data_path):
    # 接通状态统计
    all_people = callin_data['姓名'].unique()
    connection = []
    missing = []
    for p in all_people:
      con = (callin_data.loc[callin_data['姓名']== p]['通话状态']=='接通').sum()
      mis = (callin_data.loc[callin_data['姓名']== p]['通话状态']=='未接通').sum()
      connection.append(con)
      missing.append(mis)
    people_series = pd.Series(data = all_people, name = '姓名')
    connection_series = pd.Series(data = connection, name = '接通')
    missing_series = pd.Series(data = missing, name = '未接通')
    personal_calls = pd.concat([people_series, connection_series, missing_series], axis=1)
    personal_calls['电话量'] = personal_calls['接通']+personal_calls['未接通']
    personal_calls['接通率'] = personal_calls['接通']/personal_calls['电话量']
    with pd.ExcelWriter(callin_data_path, engine='openpyxl', mode='a') as writer:  
      personal_calls.to_excel(writer, sheet_name='个人接通量', index=False)

  def calc_satisfaction(self, callin_data, callin_data_path):
    # 满意度统计
    callin_data['满意度'].unique()
    all_people = callin_data['姓名'].unique()
    score_a = []
    score_b = []
    score_c = []
    for p in all_people:
      a = (callin_data.loc[callin_data['姓名']== p]['满意度']=='非常满意').sum()
      b = (callin_data.loc[callin_data['姓名']== p]['满意度']=='满意').sum()
      c = (callin_data.loc[callin_data['姓名']== p]['满意度']=='不满意').sum()
      score_a.append(a)
      score_b.append(b)
      score_c.append(c)
    people_series = pd.Series(data = all_people, name = '姓名')
    a_series = pd.Series(data = score_a, name = '非常满意')
    b_series = pd.Series(data = score_b, name = '满意')
    c_series = pd.Series(data = score_c, name = '不满意')
    personal_score = pd.concat([people_series, a_series, b_series, c_series], axis=1)
    personal_score['总评价数'] = personal_score['非常满意']+personal_score['满意']+personal_score['不满意']
    personal_score['非常满意率'] = personal_score['非常满意']/personal_score['总评价数']
    with pd.ExcelWriter(callin_data_path, engine='openpyxl', mode='a') as writer:  
      personal_score.to_excel(writer, sheet_name='个人满意度', index=False)

