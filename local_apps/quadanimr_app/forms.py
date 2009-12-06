from django import forms
from django.utils.simplejson import dumps

class PhotoForm(forms.Form):
    photo = forms.FileField(label=u'photo')
    description = forms.CharField(label=u'description', widget=forms.Textarea, required=False)
    
