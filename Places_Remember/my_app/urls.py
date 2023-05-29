from django.urls import path
from . import views


urlpatterns = [
    path('', views.login),
    path('info/', views.vk_auth_callback),
    path('google/', views.google),
    path('vk/', views.vk),
    path('addmemory/', views.addmemory, name='add_memory'),
]