from django.urls import path
from . import views

urlpatterns = [
    path('', views.hi, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.UserProfile, name='profile-page'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>', views.changeRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='del-room'),
    path('login-register/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout-view/', views.logout_view, name='log-out'),
    path('delete-comment/<str:pk>', views.deletemessage, name='delete-message'),
]
