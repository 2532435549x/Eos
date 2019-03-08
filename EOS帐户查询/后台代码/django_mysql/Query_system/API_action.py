import requests
import datetime
import random
import time
import re

class get_action_from_API(object):
    def __init__(self,account):
        self.url = 'https://api.eospark.com/api'
        self.module = 'account'
        self.account = account
        self.action = ['get_account_resource_info',
                       'get_account_balance',
                       'get_token_list',
                       'get_sub_account_info',
                       'get_account_related_trx_info']
        self.apikey = ["d59e3fe483f7b1b54a69081253343ec3","902d7f2a0c92cee44023570d047d2a20","f582bbbb014d72a90763be8859fc9078"]
        self.error_dic = {0:'成功',
                          3:'输入账号超过12位，请检查并重新输入',
                          400:'非法请求,请检查参数是否完整，接口是否调用正确',
                          403:'没有权限访问,请检查 API key 是否正确',
                          404:'EOSpark崩溃，请再次尝试',
                          429:'访问被限制超过频率限制',
                          500:'系统问题',
                          555:'检查账号是否输入正确'}

    def get_randomPAI(self):
        apikey = random.sample(self.apikey, 1)[0]
        return apikey

    def get_resource(self):#查询账户的RAM/CPU/NET等资源信息
        apikey = self.get_randomPAI()
        API = r"%s?module=%s&action=%s&apikey=%s&account=%s" % (self.url, self.module, self.action[0],apikey,self.account)
        info_return = self.get_info_corresponding(API)
        resource_info = self.resourece_balance_token_check(info_return)
        if resource_info['errno']==0:
            if resource_info['data']['unstake'] == None:
                resource_info['data']['unstake']={"cpu_amount": '0',"net_amount": '0'}
        return resource_info

    def get_balance(self):  #查询账户EOS详细信息
        apikey = self.get_randomPAI()
        API = r"%s?module=%s&action=%s&apikey=%s&account=%s" % (self.url, self.module, self.action[1], apikey, self.account)
        info_return = self.get_info_corresponding(API)
        balance_info = self.resourece_balance_token_check(info_return)
        return balance_info

    def get_tokenList(self): #查询账户代币列表
        apikey = self.get_randomPAI()
        API = r"%s?module=%s&action=%s&apikey=%s&account=%s" % (self.url, self.module, self.action[2], apikey, self.account)
        info_return = self.get_info_corresponding(API)
        tokenList_info = self.resourece_balance_token_check(info_return)
        return tokenList_info

    def get_token_action(self,recent_time):#查询账户代币交易
        apikey = self.get_randomPAI()
        page = 1
        API = r"%s?module=%s&action=%s&apikey=%s&account=%s&page=%d" % (
            self.url, self.module, self.action[4], apikey, self.account, page)
        action_info = self.get_info_corresponding(API)
        actionList_info_list = self.createAccount_tokenAction_check(action_info, self.action[4],recent_time)
        return actionList_info_list

    def resourece_balance_token_check(self, info_return):
        errorNumber = info_return['errno']
        if errorNumber==0:
            apikey = self.get_randomPAI()
            API = r"%s?module=%s&action=get_account_resource_info&apikey=%s&account=%s" % (self.url, self.module, apikey, self.account)
            check_flag = self.account_check_again()
            if check_flag == '':
                return {"errno": 555,"data":self.error_dic[555]}
            else:
                return {"errno": 0,'data':info_return['data']}
        else:
            return {"errno": errorNumber, 'data': self.error_dic[errorNumber]}

    def account_check_again(self):
        apikey = self.get_randomPAI()
        API = r"%s?module=%s&action=get_account_resource_info&apikey=%s&account=%s" % (
        self.url, self.module, apikey, self.account)
        check_return = self.get_info_further(API)
        check_flag = check_return["data"]["staked"]["cpu_weight"]
        return check_flag

    def createAccount_tokenAction_check(self, info_return, action,recent_time):
        return_info_list = []
        page =2
        info_return_errno = info_return['errno']
        if info_return_errno == 0:
            check_flag = self.account_check_again()
            if check_flag == '':
                return {"errno": 555,"data":self.error_dic[555]}
            else:
                if action == 'get_sub_account_info':
                    list_null = info_return['data']['created_list']
                elif action == 'get_account_related_trx_info':
                    list_null = info_return['data']['trace_list']
                while list_null != []:
                    for each_action in list_null:#each_action是每条交易的所有信息
                        each_action['timestamp'] = self.change_to_local(each_action['timestamp'])#把获取的时间转化为本地时间
                        each_action['quantity'] = float(each_action['quantity'])#把获取的代币数量转化成float数量
                        if each_action['timestamp'] > recent_time:
                            return_info_list.append(each_action)
                        else:
                            return {'errno':0,'data':return_info_list}
                    apikey = self.get_randomPAI()
                    API = r"%s?module=%s&action=%s&apikey=%s&account=%s&page=%d" % (
                        self.url, self.module, action, apikey, self.account, page)
                    actionList_info = self.get_info_further(API)
                    list_null = actionList_info['data']['trace_list']
                    page += 1
                return {'errno':0,'data':return_info_list}
        else:
            return {'errno':info_return_errno,'data':self.error_dic[info_return_errno]}

    def get_info_corresponding(self, API):
        try:
            infomation = requests.get(API).json()
        except:
            infomation = {"errno": 404, 'data': self.error_dic[404]}
        return infomation

    def get_info_further(self, API):
        infomation = requests.get(API).json()
        while (infomation["errno"] != 0):
            infomation = requests.get(API).json()
        return infomation

    def another_get(self):
        info1 = self.get_resource()
        info2 = self.get_balance()
        info3 = self.get_tokenList()
        return info1['data'], info2['data'], info3['data']

    def change_to_local(self,UTCtime):
        UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
        utcTime = datetime.datetime.strptime(UTCtime, UTC_FORMAT)
        est_8_time = utcTime + datetime.timedelta(hours=8)
        date = re.split(r'\.', str(est_8_time))[0]
        local_time = date
        return local_time