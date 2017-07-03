# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_auto_20170626_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistory',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
