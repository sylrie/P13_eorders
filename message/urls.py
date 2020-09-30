""" urls for message app """
from django.urls import path
from . import views

APP_NAME = 'message'

urlpatterns = [
    path('message/add', views.new_comment, name='new_comment'),
    path('message/check', views.check_comment, name='check_comment')
]