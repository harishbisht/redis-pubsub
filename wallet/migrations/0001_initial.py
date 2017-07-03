# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transation_type', models.CharField(blank=True, max_length=64, null=True, choices=[(b'Add To Wallet', b'Add To Wallet'), (b'Transfer', b'Transfer')])),
                ('transation_id', models.CharField(max_length=64, null=True, blank=True)),
                ('transaction_amount', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_success', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name=b'Email Address')),
                ('balance', models.IntegerField(default=0)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='transactionhistory',
            name='to_wallet',
            field=models.ForeignKey(related_name='Send_To', blank=True, to='wallet.Wallet', null=True),
        ),
        migrations.AddField(
            model_name='transactionhistory',
            name='user_wallet',
            field=models.ForeignKey(related_name='Owner', blank=True, to='wallet.Wallet', null=True),
        ),
    ]
