from __future__ import unicode_literals
from django.db import models

# Create your models here.
class token_action(models.Model):
    name = models.CharField('用户名',max_length=20)
    trx_id = models.CharField(max_length=100)
    status = models.CharField(max_length=15)
    timestamp = models.CharField(max_length=50)
    receiver = models.CharField(max_length=15)
    sender = models.CharField(max_length=15)
    code = models.CharField(max_length=15)
    quantity = models.FloatField()
    symbol = models.CharField(max_length=15)
    memo = models.CharField(max_length=400)
    class Meta:
        verbose_name = '用户表'  # 设置表名称在django后台显示的中文名称
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class resource_table(models.Model):
    name = models.CharField('用户名', max_length=20)
    ram_used = models.FloatField()
    ram_available = models.FloatField()
    net_used = models.FloatField()
    net_available = models.FloatField()
    net_max = models.FloatField()
    cpu_used = models.FloatField()
    cpu_available = models.FloatField()
    cpu_max = models.FloatField()
    staked_net_weight = models.CharField(max_length=50)
    staked_cpu_weight = models.CharField(max_length=50)
    unstake_net_amount = models.CharField(max_length=50)
    unstake_cpu_amount = models.CharField(max_length=50)
    balance = models.CharField(max_length=50)
    stake_to_others = models.CharField(max_length=50)
    stake_to_self = models.CharField(max_length=50)
    unstake = models.CharField(max_length=50)
    class Meta:
        verbose_name = '资产表'  # 设置表名称在django后台显示的中文名称
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class token_list_table(models.Model):
    name = models.CharField('用户名', max_length=20)
    symbol = models.CharField(max_length=15)
    code = models.CharField(max_length=15)
    balance = models.CharField(max_length=15)
    class Meta:
        verbose_name = '代币表'  # 设置表名称在django后台显示的中文名称
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class transfer_search_mail(models.Model):
    account = models.CharField('用户名', max_length=20,null=True,unique=True)
    price = models.FloatField(max_length=40,null=True)
    time = models.IntegerField(null=True)
    def __str__(self):
        return self.account