from django.shortcuts import render

# Create your views here.
def home(request):
  return render(request, 'home.html', {'usuario': 'user@name.co'})

def contact(request):
  return render(request, 'contact.html')