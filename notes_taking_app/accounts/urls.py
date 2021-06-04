from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('signup/', views.signup_view, name='signup'),
  path('home/', views.home_view, name='home_page'),
  path('change_password/', views.password_change_view, name='password_change'),
  path('check_validity/', views.check_username_validity, name='check_validity'),
]