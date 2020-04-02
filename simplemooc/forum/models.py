from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager

class Thread(models.Model):
    title = models.CharField('Title', max_length=100)
    body = models.TextField('Message')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.DO_NOTHING, verbose_name='Author', related_name='threads'
    )
    views = models.IntegerField('Views', blank=True, default=0)
    answers = models.IntegerField('Answers', blank=True, default=0)
    
    tags = TaggableManager()

    created = models.DateTimeField('Created at', auto_now_add=True)
    modified = models.DateTimeField('Modified at', auto_now=True)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['-modified']


class Reply(models.Model):
    thread = models.ForeignKey(
        Thread, models.DO_NOTHING, verbose_name='Topic', related_name='replies'
    )
    reply = models.TextField('Reply')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.DO_NOTHING, verbose_name='Author', related_name='replies'
    )
    correct = models.BooleanField('Correct?', blank=True, default=False)

    created = models.DateTimeField('Created at', auto_now_add=True)
    modified = models.DateTimeField('Modified at', auto_now=True)

    def __str__(self):
        return self.reply

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'
        ordering = ['-correct', 'created']
