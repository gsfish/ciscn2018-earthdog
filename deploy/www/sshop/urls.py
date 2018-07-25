from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='shop', permanent=True), name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('pass/reset/', views.pass_reset, name='pass_reset'),
    path('user/change/', views.user_change, name='user_change'),
    path('user/reset/', views.user_reset, name='user_reset'),
    path('user/debug/', views.user_debug, name='user_debug'),
    path('user/', views.user, name='user'),
    path('shop/', views.shop, name='shop'),
    path('info/', views.info, name='info'),
    path('pay/', views.pay, name='pay'),
    path('seckill/', views.seckill, name='seckill'),
    path('shopcar/', views.shopcar, name='shopcar'),
    path('shopcar/add/', views.shopcar_add, name='shopcar_add'),
    path('captcha/', views.captcha, name='captcha'),
]
