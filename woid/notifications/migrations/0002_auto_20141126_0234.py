# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=30, choices=[('LIKED', 'Liked'), ('COMMENTED', 'Commented'), ('FAVORITED', 'Favorited'), ('ANSWERED', 'Answered'), ('ACCEPTED_ANSWER', 'Accepted Answer'), ('ALSO_COMMENTED', 'Also Commented')]),
            preserve_default=True,
        ),
    ]
