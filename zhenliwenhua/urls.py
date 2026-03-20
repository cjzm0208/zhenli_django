"""zhenliwenhua URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path,include
from index import views
from index import admin
from index import helper
from index import app
from index import mobile
from index import new_app
# from index import helper

urlpatterns = [
    path('', views.accueil),
    path('home/', views.accueil),
    path('index/<str:type>/<int:num>/<str:name>/', views.index),
    # path('index/<str:fun>/', admin.index),
    # path('index_page/<str:fun>/<int:num>/', views.pages),
    path('login/', views.login),
    path('register/', views.register),
    path('oubile_mots/', views.oubile_mots),
    path('oubile_mots_change/', views.oubile_mots_change),
    path('oubile_mots_tel_change/', views.oubile_mots_tel_change),
    path('logout/', views.logout),
    path('accueil/<str:fun>/', admin.accueil),
    path('user/<str:fun>/<int:num>/', admin.user),
    path('helper/<str:type>/',helper.helper),
    path('helper_cur/<str:type>/',helper.helper_cur),
    path('help/<str:type>/',helper.help),
    path('tinymc/<str:fun>/',helper.tinymc),
    path('cathegorie/<str:fun>/<int:num>/', admin.cathegorie),
    path('page/<str:fun>/<int:num>/', admin.page),
    path('article/<str:fun>/<int:num>/', admin.article),
    path('comment/<str:fun>/<int:num>/', admin.comment),
    path('cours/<str:fun>/<int:num>/', admin.cours),
    path('bible/<str:fun>/<int:num>/', admin.bible),
    path('lecture/<str:fun>/<int:num>/', admin.lecture),
    path('cathe_cour/<str:fun>/<int:num>/', admin.cathe_cours),
    path('live/<str:fun>/<int:num>/', admin.live),
    path('prayer/<str:fun>/<int:num>/', admin.prayer),
    path('feedback/<str:fun>/<int:num>/', admin.feedback),
    path('app_index/<str:fun>/<int:num>/', admin.app_index),
    path('app/<str:fun>/',app.app),
    path('apps/<str:fun>/',app.apps),
    path('new_app/<str:fun>/',new_app.new_app),
    path('app_help/<str:fun>/',app.app_help),
    path('setting/<str:fun>/<str:key>/', admin.setting),
    path('statistic/<str:fun>/<str:key>/', admin.statistic),
    path('page/<str:type>/', views.page),
    path('m/<str:type>/<str:fun>/', mobile.m),
    path('m/<str:type>/<str:fun>/', mobile.m),

    # path('confirm/', views.user_confirm),
]
