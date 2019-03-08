import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_mysql.settings")# project_name 项目名称
django.setup()

import time
import multiprocessing
from Query_system import models
from Query_system.API_action import get_action_from_API
from Query_system.excelAction import readWriteExcel

def get_local_time(username):#在库中拿的本地时间
    time = models.token_action.objects.filter(name=username).values().order_by('timestamp')  # 拿到最大时间的那条数据
    recent_time = list(time)[-1]['timestamp']  # 拿到最大时间
    return recent_time

def updateInfo(account, number):
    obj_PAI_action = get_action_from_API(account)  # 生成对象
    try:
        recent_time = get_local_time(account)
    except:
        recent_time = '2017-01-01 00:00:00'
    info5 = obj_PAI_action.get_token_action(recent_time)  # 拿到交易数据
    if info5['errno'] == 0:
        info1, info2, info3 = obj_PAI_action.another_get()  # 拿到resource,balance,token_list
        while (info1 == "系统问题" or info2 == "系统问题" or info3 == "系统问题"):
            info1, info2, info3 = obj_PAI_action.another_get()  # 拿到resource,balance,token_list
        info1 = {'name': account, 'ram_used': info1['ram']['used'], 'ram_available': info1['ram']['available'],
                 'net_used': info1['net']['used'], 'net_available': info1['net']['available'],
                 'net_max': info1['net']['max'], 'cpu_used': info1['cpu']['used'],
                 'cpu_available': info1['cpu']['available'], 'cpu_max': info1['cpu']['max'],
                 'staked_net_weight': info1['staked']['net_weight'],
                 'staked_cpu_weight': info1['staked']['cpu_weight'],
                 'unstake_cpu_amount': info1['unstake']['cpu_amount'],
                 'unstake_net_amount': info1['unstake']['net_amount'], 'balance': info2['balance'],
                 'stake_to_others': info2['stake_to_others'], 'stake_to_self': info2['stake_to_self'],
                 'unstake': info2['unstake']}
        for each_action in info5['data']:
            each_action.update({'name': account})
            each_action.pop('block_num')
            each_action.pop('data_md5')
            models.token_action.objects.update_or_create(**each_action)
        models.resource_table.objects.filter(name='%s' % account).delete()
        models.token_list_table.objects.filter(name='%s' % account).delete()
        models.resource_table.objects.update_or_create(**info1)  # 存储resource,balance
        for token in info3['symbol_list']:
            token.update({'name': account})
            models.token_list_table.objects.update_or_create(**token)  # 存储token_list
        models.transfer_search_mail.objects.update_or_create(account=account)
        print("账号%s第%d次更新成功" % (account,number))
    else:
        print("账号%s第%d次没有更新成功" % (account,number))

if __name__ == '__main__':
    number = 1
    while(True):
        exlceObj = readWriteExcel()
        accountList = exlceObj.get_account()
        pool = multiprocessing.Pool(processes=4)
        for account in accountList:
            pool.apply_async(updateInfo, (account,number,))
        pool.close()
        pool.join()
        time.sleep(300)
        number+=1