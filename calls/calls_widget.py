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
    try:
      callin_data = pd.read_excel(callin_data_path, usecols=['呼叫时间', '姓名', '通话状态', '通话时长', '满意度'], dtype={'姓名': str, '通话状态': str, '通话时长': int, '满意度': str})
      callin_data['呼叫时间'] = pd.to_datetime(callin_data['呼叫时间'],format='%Y-%m-%d %H:%M:%S')   # 更改时间为统一格式
      self.calc_call_time(callin_data, callin_data_path)
      # self.calc_connection_status(callin_data, callin_data_path)
      # self.calc_satisfaction(callin_data, callin_data_path)
      self.calc_personal_info(callin_data, callin_data_path)
      self.calc_days_info(callin_data, callin_data_path)
    except Exception as e:
      logging.exception(e)
      QMessageBox.warning(self, 'warning', '计算出错，可能原因：\n \
                                            1.文件已经在WPS中打开，请先在WPS中关闭该文档；')
      return
    QMessageBox.information(self, 'info', '计算完成！')
    
  def calc_call_time(self, callin_data, callin_data_path):
    # 统计呼叫时间
    callin_data['hour'] = callin_data['呼叫时间'].apply(lambda x: time.strptime(x.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').tm_hour*2+time.strptime(x.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').tm_min//30)
    # callin_data['hour'] = callin_data['呼叫时间'].apply(lambda x: time.strptime(x,'%Y-%m-%d %H:%M:%S').tm_hour*2+time.strptime(x,'%Y-%m-%d %H:%M:%S').tm_min//30)
    callin_time_frequency = callin_data['hour'].value_counts().sort_index()
    callin_time_frequency = callin_time_frequency.rename('呼入')
    callin_time_frequency.index = callin_time_frequency.index/2
    connection_time_frequency = callin_data.loc[callin_data['通话状态'] == '接通']['hour'].value_counts().sort_index()
    connection_time_frequency = connection_time_frequency.rename('接通')
    connection_time_frequency.index = connection_time_frequency.index/2
    missing_time_frequency = callin_data.loc[callin_data['通话状态'] == '未接通']['hour'].value_counts().sort_index()
    missing_time_frequency = missing_time_frequency.rename('未接通')
    missing_time_frequency.index = missing_time_frequency.index/2
    time_frequency = pd.concat([callin_time_frequency, connection_time_frequency, missing_time_frequency], axis =1)
    time_frequency = time_frequency.fillna(0)
    time_frequency['时间'] = time_frequency.index
    time_frequency['时间'] = time_frequency['时间'].apply(lambda x: '%d:%02d-%d:%02d' % (x//1, x%1*60, (x+0.5)//1, (x+0.5)%1*60))
    time_frequency = time_frequency[['时间', '呼入', '接通', '未接通']]
    with pd.ExcelWriter(callin_data_path, engine='openpyxl', mode='a') as writer:  
      time_frequency.to_excel(writer, sheet_name='时间段统计', index=False)
  
  def calc_personal_info(self, callin_data, callin_data_path):
    all_people = callin_data['姓名'].unique()
    people_series = pd.Series(data = all_people, name = '姓名')
    # 个人接通状态统计
    connection = []
    missing = []
    for p in all_people:
      con = (callin_data.loc[callin_data['姓名']== p]['通话状态']=='接通').sum()
      mis = (callin_data.loc[callin_data['姓名']== p]['通话状态']=='未接通').sum()
      connection.append(con)
      missing.append(mis)
    connection_series = pd.Series(data = connection, name = '接通')
    missing_series = pd.Series(data = missing, name = '未接通')
    calls_series = connection_series+missing_series
    calls_series = calls_series.rename("呼入")
    connection_rate_series = connection_series/calls_series
    connection_rate_series = connection_rate_series.rename("接通率")
    # 个人满意度统计
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
    a_series = pd.Series(data = score_a, name = '非常满意')
    b_series = pd.Series(data = score_b, name = '满意')
    c_series = pd.Series(data = score_c, name = '不满意')
    personal_score = pd.concat([people_series, a_series, b_series, c_series], axis=1)
    abc_series = a_series + b_series + c_series
    abc_series = abc_series.rename('总评价数')
    a_rate_series = a_series / abc_series
    a_rate_series = a_rate_series.rename('非常满意率')
    # 个人通话时长
    connection_time = []
    for p in all_people:
      time_count = callin_data.loc[callin_data['姓名']== p]['通话时长'].sum()
      connection_time.append(time_count)
    connection_time_series = pd.Series(data = connection_time, name = '通话时长')
    # 计算参评率
    score_rate_series = abc_series/connection_series
    score_rate_series = score_rate_series.rename('参评率')
    personal_info = pd.concat([people_series, calls_series, connection_series, 
                               abc_series, a_series, a_rate_series, score_rate_series, connection_rate_series, connection_time_series], axis=1)
    personal_info = personal_info.fillna(0)
    with pd.ExcelWriter(callin_data_path, engine='openpyxl', mode='a') as writer:  
      personal_info.to_excel(writer, sheet_name='个人数据统计', index=False)
  
  def calc_days_info(self, callin_data, callin_data_path):
    callin_data['day'] = callin_data['呼叫时间'].apply(lambda x: x.strftime('%Y-%m-%d'))
    callin_time_frequency = callin_data['day'].value_counts().sort_index()
    callin_time_frequency = callin_time_frequency.rename('呼入')
    connection_time_frequency = callin_data.loc[callin_data['通话状态'] == '接通']['day'].value_counts().sort_index()
    connection_time_frequency = connection_time_frequency.rename('接通')
    connection_rate_frequency = connection_time_frequency / callin_time_frequency
    connection_rate_frequency = connection_rate_frequency.rename('接通率')
    missing_time_frequency = callin_data.loc[callin_data['通话状态'] == '未接通']['day'].value_counts().sort_index()
    missing_time_frequency = missing_time_frequency.rename('未接通')
    day_info = pd.concat([callin_time_frequency, connection_time_frequency, missing_time_frequency, connection_rate_frequency], axis =1)
    day_info = day_info.fillna(0)
    day_info['日期'] = day_info.index
    day_info = day_info[['日期', '呼入', '接通', '未接通', '接通率']]
    with pd.ExcelWriter(callin_data_path, engine='openpyxl', mode='a') as writer:  
      day_info.to_excel(writer, sheet_name='每日数据统计', index=False)

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

