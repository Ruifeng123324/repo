"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),  # 注释掉这行，避免与我们的管理后台冲突
    # 用户认证相关URL
    path('', views.index, name='index'),  # 将首页设为index
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),  # 添加个人中心的URL
    path('songs/', views.song_list, name='song_list'),
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('artists/', views.artist_list, name='artist_list'),
    # 管理后台URL
    path('management/', views.admin_dashboard, name='admin_dashboard'),
    path('management/preference/', views.user_preference, name='user_preference'),
    path('management/users/', views.user_management, name='user_management'),
    path('management/users/<int:user_id>/get/', views.user_get, name='user_get'),
    path('management/users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('management/artists/', views.artist_management, name='artist_management'),
    path('management/artists/<int:artist_id>/get/', views.artist_get, name='artist_get'),
    path('management/artists/<int:artist_id>/delete/', views.artist_delete, name='artist_delete'),
]
