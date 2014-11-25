from django.db import models
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Activity(models.Model):
    FAVORITE = u'F'
    LIKE = u'L'
    UP_VOTE = u'U'
    DOWN_VOTE = u'D'
    ACTIVITY_TYPES = (
        (FAVORITE, _(u'Favorite')),
        (LIKE, _(u'Like')),
        (UP_VOTE, _(u'Up Vote')),
        (DOWN_VOTE, _(u'Down Vote')),
        )

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(null=True, blank=True)
    question = models.IntegerField(null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _(u'Activity')
        verbose_name_plural = _(u'Activities')

    def __unicode__(self):
        return self.activity_type
