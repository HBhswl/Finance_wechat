from django.conf.urls import url
from . import views

urlpatterns = [
    url('login/wechat', views.login_wechat),
    url('login', views.login),
]
