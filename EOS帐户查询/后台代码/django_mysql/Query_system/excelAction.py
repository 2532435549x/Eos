import os
import xlrd
import xlwt
from xlutils.copy import copy


class readWriteExcel(object):
    def __init__(self):
        self.fname =r'F:/Project Pakege/Probability_analysis/account_file/account.xls'
        self.account_list = ''
        self.lenth = 0

    def get_account(self):
        filename = xlrd.open_workbook(self.fname)
        sheet = filename.sheets()[0]
        self.account_list = sheet.col_values(0, 0)
        self.len = len(self.account_list)
        return self.account_list

    def wirteInfoToExcel(self,name):
        rbook = xlrd.open_workbook(self.fname)  # 打开文件
        wbook = copy(rbook)  # 复制文件并保留格式
        w_sheet = wbook.get_sheet(0)  # 索引sheet表
        w_sheet.write(self.len, 0, name)
        wbook.save(self.fname)