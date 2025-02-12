from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileUpdateView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
