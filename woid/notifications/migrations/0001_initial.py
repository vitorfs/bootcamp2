# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.CharField(max_length=1, choices=[('LIKED', 'Liked'), ('COMMENTED', 'Commented'), ('FAVORITED', 'Favorited'), ('ANSWERED', 'Answered'), ('ACCEPTED_ANSWER', 'Accepted Answer'), ('ALSO_COMMENTED', 'Also Commented')])),
                ('is_read', models.BooleanField(default=False)),
                ('answer', models.ForeignKey(blank=True, to='questions.Answer', null=True)),
                ('feed', models.ForeignKey(blank=True, to='feed.Feed', null=True)),
                ('from_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(blank=True, to='questions.Question', null=True)),
                ('to_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
            bases=(models.Model,),
        ),
    ]
