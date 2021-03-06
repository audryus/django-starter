from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager


class Thread(models.Model):

    title = models.CharField('Titlte', max_length=100)
    slug = models.SlugField('Slug', max_length=100, unique=True)
    body = models.TextField('Message')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.DO_NOTHING,verbose_name='Autor', related_name='threads'
    )
    views = models.IntegerField('Views', blank=True, default=0)
    answers = models.IntegerField('Answers', blank=True, default=0)
    
    tags = TaggableManager()

    created = models.DateTimeField('Created at', auto_now_add=True)
    modified = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/forum/%s" % self.slug

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
        settings.AUTH_USER_MODEL, models.DO_NOTHING, verbose_name='Autor', 
        related_name='replies'
    )
    correct = models.BooleanField('Correct?', blank=True, default=False)

    created = models.DateTimeField('Created at', auto_now_add=True)
    modified = models.DateTimeField('Modified at', auto_now=True)

    def __str__(self):
        return self.reply


    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created']


def post_save_reply(created, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()
    if instance.correct:
        instance.thread.replies.exclude(pk=instance.pk).update(
            correct=False
        )

def post_delete_reply(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()

models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)
models.signals.post_delete.connect(
    post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply'
)