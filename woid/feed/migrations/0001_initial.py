# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post', models.TextField(max_length=255)),
                ('likes', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name': 'Feed',
                'verbose_name_plural': 'Feeds',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=50, blank=True)),
                ('is_private', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('create_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(to='core.Organization')),
                ('update_user', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('name', 'organization')]),
        ),
        migrations.AddField(
            model_name='feed',
            name='group',
            field=models.ForeignKey(to='feed.Group', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feed',
            name='organization',
            field=models.ForeignKey(to='core.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feed',
            name='parent',
            field=models.ForeignKey(blank=True, to='feed.Feed', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feed',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
