from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('success/',views.success,name='success'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout')
]