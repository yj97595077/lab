# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='num',
            field=models.IntegerField(verbose_name=b'\xe8\xb5\x84\xe4\xba\xa7\xe7\xbc\x96\xe5\x8f\xb7'),
        ),
    ]
