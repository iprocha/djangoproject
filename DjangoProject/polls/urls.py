'''
Created on Nov 3, 2013

@author: iprocha
'''

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from polls import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.list, name='list'),
    # ex: /polls/5/
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
    
    url(r'^list/$', views.list , name='list'),
    
    # ex: /index/5/
    url(r'^algorithm/(?P<document_id>\d+)/$', views.indexDocument, name='algorithm'),
    
    url(r'^delete/(?P<document_id>\d+)/$', views.deleteDocument, name='delete'),
)