from django.db.models import Q

def sort_fun(actionInfo, sortType,page):
    if sortType == "dateUp":
        sortResults = actionInfo.order_by('timestamp')
    elif sortType == "priceUp":
        sortResults = actionInfo.order_by('quantity')
    elif sortType == "priceDown":
        sortResults = actionInfo.order_by('quantity').reverse()
    else:
        sortResults = actionInfo.order_by('timestamp').reverse()
    return sortResults[(page-1)*100:page*100],len(list(sortResults)),sortResults

def filter_condition_fun(json_dic,data_list):
    filtrate = json_dic['filtrate']
    username = json_dic["username"]
    if filtrate['symbol']!="":
        data_list = data_list.filter(symbol=filtrate['symbol'])
    if filtrate['transactionMeans']=="transferIn":
        data_list = data_list.filter(receiver=username)
    elif filtrate['transactionMeans']=="transferOut":
        data_list = data_list.filter(sender=username)
    if filtrate['transactionPrice']['min']!=0:
        data_list = data_list.filter(quantity__gte=filtrate['transactionPrice']['min'])
    if filtrate['transactionPrice']['max']!=0:
        data_list = data_list.filter(quantity__lte=filtrate['transactionPrice']['max'])
    if filtrate['othername']!="":
        data_list = data_list.filter(Q(receiver=filtrate['othername'])|Q(sender=filtrate['othername']))
    if filtrate["time"]["startTime"]!="":
        data_list = data_list.filter(timestamp__gte=filtrate["time"]["startTime"])
    if filtrate["time"]["endTime"]!="":
        data_list = data_list.filter(timestamp__lte=filtrate["time"]["endTime"])
    return data_list

