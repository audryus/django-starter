from django import forms

class ContactCourse(forms.Form):
  name = forms.CharField(label='Name', max_length=100)
  email = forms.EmailField(label='E-mail')
  message = forms.CharField(label='Message', widget=forms.Textarea)