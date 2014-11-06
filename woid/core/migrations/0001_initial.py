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
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('verified', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=20, blank=True)),
                ('location', models.CharField(max_length=50, blank=True)),
                ('url', models.CharField(max_length=50, blank=True)),
                ('job_title', models.CharField(max_length=50, blank=True)),
                ('birthday', models.DateTimeField(null=True, blank=True)),
                ('reputation', models.IntegerField(default=0)),
                ('language', models.CharField(default=b'en', max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('name', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=30)),
                ('icon', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('token', models.CharField(max_length=255)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('resend_email_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(default='P', max_length=1, choices=[('P', 'Pending'), ('R', 'Registred'), ('C', 'Cancelled')])),
                ('create_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Invite',
                'verbose_name_plural': 'Invites',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('title', models.CharField(max_length=50, blank=True)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('url', models.CharField(max_length=50, blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('allow_domain', models.CharField(default='?', max_length=255, blank=True)),
                ('create_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationApplications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('is_visible', models.BooleanField(default=False)),
                ('application', models.ForeignKey(to='core.Application')),
                ('organization', models.ForeignKey(to='core.Organization')),
            ],
            options={
                'verbose_name': 'Organization Application',
                'verbose_name_plural': 'Organization Applications',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='organizationapplications',
            unique_together=set([('organization', 'application')]),
        ),
        migrations.AlterIndexTogether(
            name='organizationapplications',
            index_together=set([('organization', 'application')]),
        ),
        migrations.AddField(
            model_name='invite',
            name='organization',
            field=models.ForeignKey(to='core.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='organization',
            field=models.ForeignKey(to='core.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
