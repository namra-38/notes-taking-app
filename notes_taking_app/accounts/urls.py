from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
  path('login/', views.login_view, name='login'),
  path('signup/', views.signup_view, name='signup'),
  path('check_validity/', views.check_username_validity, name='check_validity'),
]