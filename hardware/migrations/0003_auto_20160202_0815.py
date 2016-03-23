# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0002_auto_20160202_0713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='num',
        ),
        migrations.AddField(
            model_name='server',
            name='number',
            field=models.CharField(default=123, max_length=256, verbose_name=b'\xe8\xb5\x84\xe4\xba\xa7\xe7\xbc\x96\xe5\x8f\xb7'),
            preserve_default=False,
        ),
    ]
