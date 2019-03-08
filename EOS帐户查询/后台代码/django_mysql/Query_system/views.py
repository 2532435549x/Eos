from Query_system import models
from Query_system.API_action import get_action_from_API
from Query_system.filtrate_function import sort_fun,filter_condition_fun
from Query_system.excelAction import readWriteExcel
from django.http import HttpResponse
from json import dumps
import json

# Create your views here.

def login(request):
    if request.method=='POST':
        postBody = request.body
        post_str_json = json.loads(postBody)
        username = post_str_json['username']
        password = post_str_json['password']
        if username =='admin' and password=='admin':
            return HttpResponse(dumps({'errno': 0},default=lambda obj: obj.__dict__), content_type='application/json')
        else:
            return HttpResponse(dumps({'errno': 1}, default=lambda obj: obj.__dict__), content_type='application/json')

def query(request):
    if request.method=='GET':
        account = str(request.GET.get('username'))
        obj_PAI_action = get_action_from_API(account)  # 生成对象
        excelObj = readWriteExcel()
        accountList = excelObj.get_account()
        if account not in accountList:
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
                excelObj.wirteInfoToExcel(account)#把新添加的账号加入到EXCEL表中
                action_data = models.token_action.objects.filter(name="%s" % account).values().order_by('timestamp').reverse()
                action_number = len(list(action_data))
                resource_data = models.resource_table.objects.filter(name="%s" % account).values()
                symbol = "no"
                token_data, token_variety = get_token_variety(account,symbol,action_data)
                token_in_out_list = calculate_amount(token_variety, action_data, account)
                return HttpResponse(dumps(
                    {'errno': info5['errno'], "action_number": action_number, "transfer": list(action_data[:100]),
                     "resource_data": list(resource_data), "token_data": token_data, "token_in_out_list":token_in_out_list, "transferForExcel":list(action_data),"errorInfo":None},
                    default=lambda obj: obj.__dict__), content_type='application/json')
            else:
                action_data = info5['data']
                action_number = 0
                return HttpResponse(dumps({'errno': info5['errno'],"action_number":action_number,"transfer":[],
                                           "resource_data":{},"token_data":{},"errorInfo":action_data}, default=lambda obj: obj.__dict__),
                                    content_type='application/json')
        else:
            action_data = models.token_action.objects.filter(name="%s" % account).values().order_by(
                'timestamp').reverse()
            action_number = len(list(action_data))
            resource_data = models.resource_table.objects.filter(name="%s" % account).values()
            symbol = "no"
            token_data, token_variety = get_token_variety(account, symbol, action_data)
            token_in_out_list = calculate_amount(token_variety, action_data, account)
            return HttpResponse(dumps(
                {'errno': 0, "action_number": action_number, "transfer": list(action_data[:100]),
                 "resource_data": list(resource_data), "token_data": token_data, "token_in_out_list": token_in_out_list,
                 "transferForExcel": list(action_data), "errorInfo": None},
                default=lambda obj: obj.__dict__), content_type='application/json')
    else:
        return HttpResponse(dumps({"transfer": 0}, default=lambda obj: obj.__dict__),
                            content_type='application/json')

def get_page(request):
    if request.method=='POST':
        postBody = request.body
        post_str_json = json.loads(postBody)
        username = post_str_json['username']
        page = post_str_json['page']
        if post_str_json['status']==0:
            action_data = models.token_action.objects.filter(name="%s" % username).values().order_by('timestamp').reverse()
            action_number = len(list(action_data))
            action_data =action_data[(page-1)*100:page*100]
            return HttpResponse(dumps({'errno': 0,"action_number": action_number,"transfer":list(action_data)},
                                      default=lambda obj: obj.__dict__),content_type='application/json')
        else:
            action_data, action_number, sortResults_all = Turn_page_filtrate(post_str_json)
            return HttpResponse(dumps({'errno': 0, "action_number": action_number, "transfer": list(action_data),"transferForExcel":list(action_data)},
                                      default=lambda obj: obj.__dict__), content_type='application/json')
    else:
        return HttpResponse(dumps({"transfer": 0}, default=lambda obj: obj.__dict__),
                            content_type='application/json')

def get_filtrate(request):
    if request.method=='POST':
        postBody = request.body
        post_str_json = json.loads(postBody)
        username = post_str_json['username']
        symbol = post_str_json['filtrate']['symbol']
        action_data, action_number, sortResults_all = Turn_page_filtrate(post_str_json)
        token_data, token_variety = get_token_variety(username, symbol,sortResults_all)
        token_in_out_list = calculate_amount(token_variety, sortResults_all, username)
        return HttpResponse(dumps({'errno': 0, "action_number": action_number, "transfer": list(action_data), "token_in_out_list":token_in_out_list,"transferForExcel":list(sortResults_all)},
                                  default=lambda obj: obj.__dict__), content_type='application/json')
    else:
        return HttpResponse(dumps({"transfer": 0}, default=lambda obj: obj.__dict__),
                            content_type='application/json')

def Turn_page_filtrate(post_str_json):
    username = post_str_json['username']
    sortType = post_str_json['filtrate']['sortType']
    current_page = post_str_json['page']
    action_data = models.token_action.objects.filter(name=username).values()
    data_list = filter_condition_fun(post_str_json, action_data)
    action_data, action_number, sortResults_all = sort_fun(data_list, sortType, current_page)
    return action_data, action_number, sortResults_all

def get_token_variety(username,symbol,sortResults_all):
    token_variety=[]
    token_data = models.token_list_table.objects.filter(name="%s" % username).values()
    token_data = list(token_data)
    if symbol=="no":
        for token in token_data:
            token_variety.append(token['symbol'])
    elif symbol=="":
        for token in sortResults_all:
            token_variety.append(token['symbol'])
            token_variety = sorted(set(token_variety), key=token_variety.index)
    else:
        token_variety.append(symbol)
    return token_data, token_variety

def calculate_amount(token_variety, actionInfo, username):
    token_in_out_list = []
    for token in token_variety:
        token_in_out_dict = {}
        action_data = actionInfo.filter(symbol=token)
        action_in = action_data.filter(receiver=username)
        action_out = action_data.filter(sender=username)
        amount_in = 0
        amount_out = 0
        for data in action_in:
            amount_in += data['quantity']
        for data in action_out:
            amount_out += data["quantity"]
        token_in_out_dict.update({"symbol":token,"amount_in":round(amount_in,4),"amount_out":round(amount_out,4)})
        token_in_out_list.append(token_in_out_dict)
    return token_in_out_list