from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from simplemooc.core.mail import send_mail_template

class CourseManager(models.Manager):
  def search(self, query):
    return self.get_queryset().filter(
      models.Q(name__icontains=query) | \
      models.Q(description__icontains=query)
    )


class Course(models.Model):
  name = models.CharField('Name', max_length=100)
  slug = models.SlugField('Shortcut')
  description = models.TextField('Description', blank=True)
  about = models.TextField('About', blank=True)
  start_date = models.DateField('Start date', null=True, blank=True)
  photo = models.ImageField(upload_to='courses/images', verbose_name='Photo', null=True, blank=True)
  created_at = models.DateTimeField('Created on', auto_now_add=True)
  updated_at = models.DateTimeField('Last updated', auto_now=True)
  objects = CourseManager()

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return "/courses/%s" % self.slug

  def release_lessons(self):
    today = timezone.now().date()
    return self.lessons.filter(release_date__gte=today)

  class Meta:
    verbose_name="Course to learn"
    verbose_name_plural="Courses to learn more"

class Enrollment(models.Model):
  STATUS_CHOICES = (
    (0, 'Pending'),
    (1, 'Approved'),
    (2, 'Canceled'),
  )

  user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING,
    verbose_name='User',
    related_name='enrollments'
  )
  course = models.ForeignKey(Course, models.DO_NOTHING,
    verbose_name='Course', related_name='enrollments'
  )
  status = models.IntegerField(
    'Status', choices=STATUS_CHOICES, default=1, blank=True
  )

  created_at = models.DateTimeField('Created at', auto_now_add=True)
  updated_at = models.DateTimeField('Updated at', auto_now=True)
  objects = CourseManager()
  
  def active(self):
    self.status = 1
    self.save()

  class Meta:
    verbose_name = 'Enrollment'
    verbose_name_plural = 'Enrollments'
    unique_together = (('user', 'course'),)

class Announcement(models.Model):
  course = models.ForeignKey(
    Course, models.DO_NOTHING,verbose_name='Course', related_name='announcements'
  )
  title = models.CharField('Title', max_length=100)
  content = models.TextField('Content')

  created_at = models.DateTimeField('Created at', auto_now_add=True)
  updated_at = models.DateTimeField('Updated at', auto_now=True)

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = 'Announcement'
    verbose_name_plural = 'Announcements'
    ordering = ['-created_at']


class Comment(models.Model):
  announcement = models.ForeignKey(
    Announcement, models.DO_NOTHING, verbose_name='announcement', related_name='comments'
  )
  user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, verbose_name='user')
  comment = models.TextField('Comment')

  created_at = models.DateTimeField('Criado em', auto_now_add=True)
  updated_at = models.DateTimeField('Atualizado em', auto_now=True)

  class Meta:
    verbose_name = 'Comment'
    verbose_name_plural = 'Comments'
    ordering = ['created_at']


def post_save_announcement(instance, created, **kwargs):
  if created:
    subject = instance.title
    context = {
      'announcement': instance
    }
    template_name = 'courses/announcement_mail.html'
    enrollments = Enrollment.objects.filter(
      course=instance.course, status=1
    )
    for enrollment in enrollments:
      recipient_list = [enrollment.user.email]
      send_mail_template(subject, template_name, context, recipient_list)

models.signals.post_save.connect(
  post_save_announcement, sender=Announcement,
  dispatch_uid='post_save_announcement'
)

class Lesson(models.Model):
  name = models.CharField('Name', max_length=100)
  description = models.TextField('Description', blank=True)
  number = models.IntegerField('Order', blank=True, default=0)
  release_date = models.DateField('Release date', blank=True, null=True)

  course = models.ForeignKey(Course, models.DO_NOTHING, verbose_name='Course', related_name='lessons')

  created_at = models.DateTimeField('Created at', auto_now_add=True)
  updated_at = models.DateTimeField('Updated at', auto_now=True)

  def __str__(self):
    return self.name

  def is_available(self):
    if self.release_date:
      today = timezone.now().date()
      return self.release_date >= today
    return False

  class Meta:
    verbose_name = 'Lesson'
    verbose_name_plural = 'Lessons'
    ordering = ['number']


class Material(models.Model):
  name = models.CharField('Name', max_length=100)
  embedded = models.TextField('Vídeo embedded', blank=True)
  file = models.FileField(upload_to='lessons/materials', blank=True, null=True)

  lesson = models.ForeignKey(Lesson, models.DO_NOTHING, verbose_name='Lesson', related_name='materials')

  def is_embedded(self):
    return bool(self.embedded)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Material'
    verbose_name_plural = 'Materials'
