from django.db import models
from django.urls import reverse

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

  class Meta:
    verbose_name="Course to learn"
    verbose_name_plural="Courses to learn more"
