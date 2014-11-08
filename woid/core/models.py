from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import urllib, hashlib

class Application(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    description = models.CharField(max_length=30)
    url = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)

    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')

    def __unicode__(self):
        return self.name


class Organization(models.Model):
    ALLOW_ALL_DOMAINS = u'*'
    DENY_ALL_DOMAINS = u'?'

    name = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=50, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User, related_name='+')
    update_date = models.DateTimeField(null=True, blank=True)
    update_user = models.ForeignKey(User, related_name='+', null=True, blank=True)
    allow_domain = models.CharField(max_length=255, blank=True, default=DENY_ALL_DOMAINS)

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')

    def __unicode__(self):
        return self.name

    def get_applications(self):
        return OrganizationApplications.objects.filter(organization__id=self.pk)

    def get_invites(self):
        return Invite.objects.filter(organization__id=self.pk)


class OrganizationApplications(models.Model):
    organization = models.ForeignKey(Organization)
    application = models.ForeignKey(Application)
    order = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Organization Application')
        verbose_name_plural = _('Organization Applications')
        unique_together = (('organization', 'application'),)
        index_together = [['organization', 'application'],]

    def __unicode__(self):
        return u'{0}_{1}'.format(self.organization.name, self.application.name)


class Invite(models.Model):
    PENDING = u'P'
    REGISTRED = u'R'
    CANCELLED = u'C'
    STATUS_VALUES = (
        (PENDING, u'Pending'),
        (REGISTRED, u'Registred'),
        (CANCELLED, u'Cancelled'),
        )

    organization = models.ForeignKey(Organization)
    email = models.EmailField()
    token = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User)
    resend_email_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_VALUES, default=PENDING)
    
    class Meta:
        verbose_name = _('Invite')
        verbose_name_plural = _('Invites')

    def __unicode__(self):
        return u'{0}_{1}'.format(self.organization.name, self.email)


class Account(models.Model):
    user = models.OneToOneField(User)
    organization = models.ForeignKey(Organization)
    verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=50, blank=True)
    url = models.CharField(max_length=50, blank=True)
    job_title = models.CharField(max_length=50, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    reputation = models.IntegerField(default=0)
    language = models.CharField(max_length=5, default='en')

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
            url = "http://" + str(self.url)
        return url 

    def get_picture(self):
        no_picture = settings.NO_PICTURE
        try:
            gravatar_url = u'http://www.gravatar.com/avatar/{0}?{1}'.format(
                hashlib.md5(self.user.email.lower()).hexdigest(),
                urllib.urlencode({'d':no_picture, 's':'128'}))
            return gravatar_url
        except Exception, e:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

def save_user_account(sender, instance, **kwargs):
    instance.account.save()

post_save.connect(create_user_account, sender=User)
post_save.connect(save_user_account, sender=User)