from django.db import models
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Notification(models.Model):
    LIKED = u'LIKED'
    COMMENTED = u'COMMENTED'
    FAVORITED = u'FAVORITED'
    ANSWERED = u'ANSWERED'
    ACCEPTED_ANSWER = u'ACCEPTED_ANSWER'
    ALSO_COMMENTED = u'ALSO_COMMENTED'
    NOTIFICATION_TYPES = (
        (LIKED, _(u'Liked')),
        (COMMENTED, _(u'Commented')),
        (FAVORITED, _(u'Favorited')),
        (ANSWERED, _(u'Answered')),
        (ACCEPTED_ANSWER, _(u'Accepted Answer')),
        (ALSO_COMMENTED, _(u'Also Commented')),
        )

    _LIKED_TEMPLATE = u'<a href="/{0}/">{1}</a> liked your post: <a href="/feed/{2}/">{3}</a>'
    _COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> commented on your post: <a href="/feed/{2}/">{3}</a>'
    _FAVORITED_TEMPLATE = u'<a href="/{0}/">{1}</a> favorited your question: <a href="/questions/{2}/">{3}</a>'
    _ANSWERED_TEMPLATE = u'<a href="/{0}/">{1}</a> answered your question: <a href="/questions/{2}/">{3}</a>'
    _ACCEPTED_ANSWER_TEMPLATE = u'<a href="/{0}/">{1}</a> accepted your answer: <a href="/questions/{2}/">{3}</a>'
    _ALSO_COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> also commentend on the post: <a href="/feed/{2}/">{3}</a>'

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey('feed.Feed', null=True, blank=True)
    question = models.ForeignKey('questions.Question', null=True, blank=True)
    answer = models.ForeignKey('questions.Answer', null=True, blank=True)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _(u'Notification')
        verbose_name_plural = _(u'Notifications')
        ordering = ('-date',)

    def __unicode__(self):
        return '{0}_{1}_{2}'.format(from_user.username, to_user.username, notification_type)

    def render(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.FAVORITED:
            return self._FAVORITED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.question.pk,
                escape(self.get_summary(self.question.title))
                )
        elif self.notification_type == self.ANSWERED:
            return self._ANSWERED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.question.pk,
                escape(self.get_summary(self.question.title))
                )
        elif self.notification_type == self.ACCEPTED_ANSWER:
            return self._ACCEPTED_ANSWER_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.answer.question.pk,
                escape(self.get_summary(self.answer.description))
                )
        elif self.notification_type == self.ALSO_COMMENTED:
            return self._ALSO_COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        else:
            return _(u'Ooops! Something went wrong.')

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])
        else:
            return value

    @staticmethod
    def notify_liked(user, feed):
        if user != feed.user:
            notification = Notification(notification_type=Notification.LIKED, from_user=user, to_user=feed.user, feed=feed)
            notification.save()

    @staticmethod
    def unotify_liked(user, feed):
        if user != feed.user:
            notification = Notification.objects.filter(notification_type=Notification.LIKED, from_user=user, to_user=feed.user, feed=feed)
            notification.delete()

    @staticmethod
    def notify_commented(user, feed):
        if user != feed.user:
            notification = Notification(notification_type=Notification.COMMENTED, from_user=user, to_user=feed.user, feed=feed)
            notification.save()

    @staticmethod
    def notify_also_commented(user, feed):
        comments = feed.get_comments()
        users = []
        for comment in comments:
            if comment.user != user and comment.user != feed.user:
                users.append(comment.user.pk)
        users = list(set(users))
        for user in users:
            notification = Notification(notification_type=Notification.ALSO_COMMENTED, from_user=user, to_user=User(id=user), feed=feed)
            notification.save()
