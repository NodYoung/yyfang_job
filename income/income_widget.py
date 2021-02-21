from .ui_income_widget import Ui_IncomeWidget
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import numpy as np
import pandas as pd
import time
import logging

# 本应用主要用于统计客服的转化收益。
# 统计准则是以客服支持后10天以内的计入客服转化收益。
class IncomeWidget(QWidget):
  def __init__(self):
    super().__init__()
    self.ui = Ui_IncomeWidget()
    self.ui.setupUi(self)
    # self.ui.lineEdit_workorder_filepath.setText('D:/yyfang/210216/data/income_sample/工单报表.xlsx')
    # self.ui.lineEdit_session_filepath.setText('D:/yyfang/210216/data/income_sample/会话记录报表.xlsx')
    # self.ui.lineEdit_fee_filepath.setText('D:/yyfang/210216/data/income_sample/学费报表.xlsx')
    pd.set_option('display.max_columns', None)

  @pyqtSlot()
  def on_pushButton_workorder_browse_clicked(self):
    filepath, _ = QFileDialog.getOpenFileName(self, 'Open file', self.ui.lineEdit_workorder_filepath.text(), 'Excel (*.xls *.xlsx)')
    if filepath:
      self.ui.lineEdit_workorder_filepath.setText(filepath)

  @pyqtSlot()
  def on_pushButton_session_browse_clicked(self):
    filepath, _ = QFileDialog.getOpenFileName(self, 'Open file', self.ui.lineEdit_session_filepath.text(), 'Excel (*.xls *.xlsx)')
    if filepath:
      self.ui.lineEdit_session_filepath.setText(filepath)

  @pyqtSlot()
  def on_pushButton_fee_browse_clicked(self):
    filepath, _ = QFileDialog.getOpenFileName(self, 'Open file', self.ui.lineEdit_fee_filepath.text(), 'Excel (*.xls *.xlsx)')
    if filepath:
      self.ui.lineEdit_fee_filepath.setText(filepath)

  @pyqtSlot()
  def on_pushButton_calc_clicked(self):
    input_workorder_path = self.ui.lineEdit_workorder_filepath.text()
    input_session_records_path = self.ui.lineEdit_session_filepath.text()
    input_tuition_fee_path = self.ui.lineEdit_fee_filepath.text()
    try:
      logging.info('第一步：把《会话记录报表》中有电话的筛出来，并存入<有电话号>sheet中')
      has_phone_number_data = self.calc_has_phone_number(input_session_records_path)
      logging.info('第二步：把《会话记录报表》中有效数据合并到工单报表')
      merge_data = self.merge_data(has_phone_number_data, input_workorder_path)
      logging.info('第三步：把《学费报表》中金额大于0的数据抽取出来，按金额降序')
      profitable_tuition_fee_data = self.calc_profitable_tuition_fee(input_tuition_fee_path, input_workorder_path)
      logging.info('第四步：把profitable_tuition_fee数据和merge数据通过手机号进行合并')
      merge_money_data = self.merge_money_data(merge_data, profitable_tuition_fee_data, input_workorder_path)
      logging.info('第五步：把merge_money数据中符合时间差的数据抽离出来')
      valid_income_data = self.extract_valid_income_data(merge_money_data, input_workorder_path)
      logging.info('第六步：统计每个人的金额')
      self.calc_personal_income(valid_income_data, input_workorder_path)
    except Exception as e:
      logging.exception(e)
      QMessageBox.warning(self, 'warning', '计算过程出错，请查看log具体错误信息')
      return
    QMessageBox.information(self, 'info', '计算完成！')

  def calc_has_phone_number(self, input_session_records_path):
    session_records_data = pd.read_excel(input_session_records_path, usecols=['会话ID', '最后接待客服', '会话结束时间', '电话'], dtype={'会话ID': str, '最后接待客服': str, '电话': str})
    session_records_data['工单生成时间'] = pd.to_datetime(session_records_data['会话结束时间'],format= '%Y-%m-%d %H:%M:%S')   # 更改时间为统一格式
    has_phone_number_data = session_records_data.loc[session_records_data['电话'].notnull()].copy()
    s = has_phone_number_data['电话'].str.split(';', expand=True).apply(pd.Series, 1).stack()
    s.index = s.index.droplevel(-1)
    s.name = '电话'
    del has_phone_number_data['电话']
    has_phone_number_data = has_phone_number_data.join(s)
    has_phone_number_data = has_phone_number_data[['会话ID', '最后接待客服', '会话结束时间', '电话']]
    with pd.ExcelWriter(input_session_records_path, engine='openpyxl', mode='a') as writer:
      has_phone_number_data.to_excel(writer, sheet_name='有电话号')
    return has_phone_number_data

  def merge_data(self, has_phone_number_data, input_workorder_path):
    workorder_data = pd.read_excel(input_workorder_path, usecols=['工单号', '创建人', '工单生成时间', '客户电话'], dtype={'工单号': str, '创建人': str, '客户电话': str})
    workorder_data['工单生成时间'] = pd.to_datetime(workorder_data['工单生成时间'],format= '%Y-%m-%d %H:%M:%S')   # 更改时间为统一格式
    # logging.info(workorder_data.head())
    valid_session_records_data = has_phone_number_data.rename(columns={'会话ID': '工单号', '最后接待客服': '创建人', '会话结束时间':'工单生成时间', '电话':'客户电话'})
    workorder_data_copy = workorder_data.copy()
    merge_data = pd.concat([workorder_data_copy, valid_session_records_data], axis = 0)
    with pd.ExcelWriter(input_workorder_path, engine='openpyxl', mode='a') as writer:
      merge_data.to_excel(writer, sheet_name='1合并会话记录', index=False)
    return merge_data

  def calc_profitable_tuition_fee(self, input_tuition_fee_path, input_workorder_path):
    try:
      tuition_fee_data = pd.read_excel(input_tuition_fee_path, usecols=['手机号', '收款/退款金额', '收款/退款日期'], dtype={'手机号': str, '收款/退款金额': float})
    except ValueError as e:
      logging.exception(e)
      QMessageBox.warning(self, 'warning', '%s 读取数据失败，解决方法：使用wps打开数据，并另存为' % input_tuition_fee_path)
      raise Exception("读取数据失败")
    # check data is not null
    if tuition_fee_data['手机号'].isnull().sum() >= len(tuition_fee_data['手机号'].index):
      raise Exception("不合理数据：学费数据手机号全为空")
    tuition_fee_data['收款/退款日期'] = pd.to_datetime(tuition_fee_data['收款/退款日期'],format= '%Y-%m-%d %H:%M:%S')   # 更改时间为统一格式
    # 同一个手机号有多次订单，合并多次订单金额，使用最早的订单日期
    # profitable_tuition_fee_data = tuition_fee_data.groupby('手机号').agg({'收款/退款金额': np.sum, '收款/退款日期': np.min}).reset_index()
    # profitable_tuition_fee_data = profitable_tuition_fee_data.rename(columns={'手机号': '客户电话'})
    # profitable_tuition_fee_data = profitable_tuition_fee_data.loc[profitable_tuition_fee_data['收款/退款金额'] > 0].copy()
    # profitable_tuition_fee_data = profitable_tuition_fee_data.sort_values(by=['收款/退款金额'], ascending=False)
    # profitable_tuition_fee_data = profitable_tuition_fee_data[['客户电话', '收款/退款金额', '收款/退款日期']]
    # 同一个手机号有多次订单，只保留最大的那一笔
    profitable_tuition_fee_data = tuition_fee_data.loc[tuition_fee_data['收款/退款金额']>0].copy()
    profitable_tuition_fee_data = profitable_tuition_fee_data.sort_values(by=['收款/退款金额'], ascending=False)
    profitable_tuition_fee_data = profitable_tuition_fee_data.drop_duplicates('手机号')   # 同一个手机号有多次订单，只保留金额最大的一笔。。。
    profitable_tuition_fee_data = profitable_tuition_fee_data.rename(columns={'手机号': '客户电话'})
    s = profitable_tuition_fee_data['客户电话'].str.split('/').apply(pd.Series, 1).stack()
    s.index = s.index.droplevel(-1) # to line up with df's index
    s.name = '客户电话'
    del profitable_tuition_fee_data['客户电话']
    profitable_tuition_fee_data = profitable_tuition_fee_data.join(s)
    profitable_tuition_fee_data = profitable_tuition_fee_data[['客户电话', '收款/退款金额', '收款/退款日期']]
    with pd.ExcelWriter(input_workorder_path, engine='openpyxl', mode='a') as writer:
      profitable_tuition_fee_data.to_excel(writer, sheet_name='2学费大于零', index=False)
    return profitable_tuition_fee_data

  def merge_money_data(self, merge_data, profitable_tuition_fee_data, input_workorder_path):
    # valid_tuition_fee_data = profitable_tuition_fee_data.rename(columns={'手机号': '客户电话'})
    # valid_tuition_fee_data['客户电话'] = valid_tuition_fee_data['客户电话'].apply(lambda x: '%s' % (str(x)))
    # valid_tuition_fee_data = valid_tuition_fee_data.drop_duplicates('客户电话')
    # s = valid_tuition_fee_data['客户电话'].str.split('/').apply(pd.Series, 1).stack()
    # s.index = s.index.droplevel(-1) # to line up with df's index
    # s.name = '客户电话'
    # del valid_tuition_fee_data['客户电话']
    # valid_tuition_fee_data = valid_tuition_fee_data.join(s)
    merge_data = merge_data.sort_values(by=['工单生成时间'], ascending=True)  # 同一个电话多次打入，去重，算最先接的那个人的
    merge_data = merge_data.drop_duplicates('客户电话')
    merge_money_data = pd.merge(left = merge_data, right = profitable_tuition_fee_data, how = 'inner', on = ['客户电话'])
    with pd.ExcelWriter(input_workorder_path, engine='openpyxl', mode='a') as writer:
      merge_money_data.to_excel(writer, sheet_name='3合并学费', index=False)
    return merge_money_data
  
  def extract_valid_income_data(self, merge_money_data, input_workorder_path):
    valid_income_data = merge_money_data.loc[merge_money_data['收款/退款日期'].notnull()].copy()
    # logging.info(valid_income_data.dtypes)
    valid_income_data['时间差'] = valid_income_data['收款/退款日期'] - valid_income_data['工单生成时间']
    valid_income_data = valid_income_data.loc[(valid_income_data['时间差'] >= pd.Timedelta(0,'D')) &  (valid_income_data['时间差'] <= pd.Timedelta(10,'D'))].copy()
    valid_income_data['时间差'] = valid_income_data['时间差'].astype(str)
    with pd.ExcelWriter(input_workorder_path, engine='openpyxl', mode='a') as writer:
      valid_income_data.to_excel(writer, sheet_name='4小于十天', index=False)
    return valid_income_data

  def calc_personal_income(self, valid_income_data, input_workorder_path):
    valid_income_data = valid_income_data.sort_values(by=['工单生成时间'], ascending=True)
    valid_income_data = valid_income_data.drop_duplicates('客户电话')
    all_people = valid_income_data['创建人'].unique()
    all_money = []
    for p in all_people:
        m = valid_income_data.loc[valid_income_data['创建人']== p]['收款/退款金额'].sum()
        all_money.append(m)
    people = pd.Series(data = all_people, name = '创建人')
    money = pd.Series(data = all_money, name = '金额')
    personal_money = pd.concat([people, money], axis=1)
    personal_money = personal_money.sort_values(by=['金额'], ascending=False)
    with pd.ExcelWriter(input_workorder_path, engine='openpyxl', mode='a') as writer:
      personal_money.to_excel(writer, sheet_name='5个人统计', index=False)
