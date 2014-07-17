'''
Created on Nov 5, 2013

@author: iprocha
'''
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Selecione um arquivo',
        help_text='max. 42 megabytes'
    )
        