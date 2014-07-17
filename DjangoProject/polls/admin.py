'''
Created on Oct 29, 2013

@author: iprocha
'''

from django.contrib import admin
from polls.models import Question
from polls.models import Choice
from polls.models import Document

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],
                              'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')
    
    
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Document)