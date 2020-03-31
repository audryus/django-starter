from django.shortcuts import render, get_object_or_404

from .models import Course
from .forms import ContactCourse
 
def courses(request):
  courses = Course.objects.all()
  template_name = 'courses/index.html'
  context = {
    'courses': courses
  }
  return render(request, template_name, context)

def detail(request, slug):
  course = get_object_or_404(Course, slug=slug)
  context = {
    'course': course
  }
  template_name = 'courses/details.html'
  if request.method == 'POST':
    form = ContactCourse(request.POST)
    if form.is_valid():
      context['is_valid'] = True
      form = ContactCourse()
  else:
    form = ContactCourse()
  
  context['form'] = form
  return render(request, template_name, context)