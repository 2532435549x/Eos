# Generated by Django 2.1.5 on 2019-01-24 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='resource_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='用户名')),
                ('ram_used', models.FloatField()),
                ('ram_available', models.FloatField()),
                ('net_used', models.FloatField()),
                ('net_available', models.FloatField()),
                ('net_max', models.FloatField()),
                ('cpu_used', models.FloatField()),
                ('cpu_available', models.FloatField()),
                ('cpu_max', models.FloatField()),
                ('staked_net_weight', models.CharField(max_length=50)),
                ('staked_cpu_weight', models.CharField(max_length=50)),
                ('unstake_net_amount', models.CharField(max_length=50)),
                ('unstake_cpu_amount', models.CharField(max_length=50)),
                ('balance', models.CharField(max_length=50)),
                ('stake_to_others', models.CharField(max_length=50)),
                ('stake_to_self', models.CharField(max_length=50)),
                ('unstake', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '资产表',
                'verbose_name_plural': '资产表',
            },
        ),
        migrations.CreateModel(
            name='token_action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='用户名')),
                ('trx_id', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=15)),
                ('timestamp', models.CharField(max_length=50)),
                ('receiver', models.CharField(max_length=15)),
                ('sender', models.CharField(max_length=15)),
                ('code', models.CharField(max_length=15)),
                ('quantity', models.FloatField()),
                ('symbol', models.CharField(max_length=15)),
                ('memo', models.CharField(max_length=400)),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.CreateModel(
            name='token_list_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='用户名')),
                ('symbol', models.CharField(max_length=15)),
                ('code', models.CharField(max_length=15)),
                ('balance', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': '代币表',
                'verbose_name_plural': '代币表',
            },
        ),
        migrations.CreateModel(
            name='transfer_search_mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=20, null=True, unique=True, verbose_name='用户名')),
                ('price', models.FloatField(max_length=40, null=True)),
                ('time', models.IntegerField(null=True)),
            ],
        ),
    ]
