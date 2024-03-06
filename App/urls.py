from django.conf import settings
from App import views
from django.contrib import admin
from django.urls import path,  include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *

#Django Admin site customization
admin.site.site_title = "MusicPlayer Admin"
admin.site.index_title = "Welcome to MusicPalyer"


urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path("login", views.login, name="login"),    
    path("list",musiclist.as_view(),name='list'),
    path("list/<int:pk>/",musicdetail.as_view(),name='detail'),
    path("home", views.home, name="home"),
    #path("home", views.index, name="index"),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)