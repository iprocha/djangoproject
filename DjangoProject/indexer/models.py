from django.db import models
from django import forms

# Create your models here.
class RawDocument(forms.Form):
    document = forms.FileField()
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question_text


