import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_mysql.settings")# project_name 项目名称
django.setup()
from Query_system import models
account = 'games.eos'
action_data = models.token_action.objects.filter(name="%s" % account).values().order_by('timestamp').reverse()
action_number = len(list(action_data))
print(action_number)
'''
import xlrd
class readWriteExcel(object):
    def __init__(self):
        self.fname =r'D:/123456.xlsx'
        self.account_list = ''
        self.lenth = 0

    def get_account(self,num):
        filename = xlrd.open_workbook(self.fname)
        sheet = filename.sheets()[0]
        self.account_list = sheet.col_values(num, 0)
        self.len = len(self.account_list)
        return self.account_list
num1 = 0
num2 =1
list = []
a = readWriteExcel()
info = a.get_account(num1)
info2 = a.get_account(num2)
for x, y in zip(info, info2):
    str = x+"/"+y
    list.append(str)
print(list)'''