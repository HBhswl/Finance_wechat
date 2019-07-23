from django.conf.urls import url
from . import views

urlpatterns = [
    url('login/wechat', views.login_wechat),
    url('login', views.login),
    url('my/profile/modify', views.modify_my_profile),
    url('my/profile', views.get_my_profile),
]
