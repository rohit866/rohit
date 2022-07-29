from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    url('index', views.home, name='home'),
    url('contact', views.contact, name='contact'),
    url('news', views.news, name='news'),
    url('prediction', views.prediction, name='prediction'),
    path('<str:tid>', views.search, name='predict'),
    path('predicts/', views.predicts, name='predicts')
]
    
