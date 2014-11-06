from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.html import escape
from woid.activities.models import Activity
from woid.core.models import Organization
import bleach

class Group(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(Organization)
    title = models.CharField(max_length=50, blank=True)
    is_private = models.BooleanField(default=False)
    users = models.ManyToManyField(User)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User, related_name='+')
    update_date = models.DateTimeField(null=True, blank=True)
    update_user = models.ForeignKey(User, related_name='+', null=True, blank=True)

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        unique_together = (('name', 'organization'),)

    def __unicode__(self):
        return self.name    

class Feed(models.Model):
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)
    group = models.ForeignKey(Group, null=True)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=255)
    parent = models.ForeignKey('Feed', null=True, blank=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')
        ordering = ('-date',)

    def __unicode__(self):
        return self.post

    @staticmethod
    def get_feeds(organization, group=None, from_feed=None):
        feeds = Feed.objects.filter(parent=None, organization=organization, group=group)
        if from_feed is not None:
            feeds = feeds.filter(id__lte=from_feed)
        return feeds

    @staticmethod
    def get_feeds_after(feed, organization, group=None):
        feeds = Feed.objects.filter(parent=None, id__gt=feed, organization=organization, group=group)
        return feeds

    def get_comments(self):
        return Feed.objects.filter(parent=self).order_by('date')

    def calculate_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, feed=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, feed=self.pk)
        return likes

    def get_likers(self):
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers

    def calculate_comments(self):
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return self.comments

    def comment(self, user, post):
        feed_comment = Feed(user=user, post=post, parent=self, organization=self.organization, group=self.group)
        feed_comment.save()
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return feed_comment

    def linkfy_post(self):
        return bleach.linkify(escape(self.post))