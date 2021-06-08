from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('signup/', views.signup_view, name='signup'),
  path('update-profile/', views.profile_update_view, name='update_profile'),
  path('home/', views.home_view, name='home_page'),
  path('change-password/', views.password_change_view, name='password_change'),
  path('check-validity/', views.check_username_validity, name='check_validity'),
  path('password-reset/', views.password_reset_view, name='password_reset'),
]

# BUILT-IN PASSWORD RESET PATTERNS
urlpatterns += [

  path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'
  ),

  path('reset-password-sent/', 
    auth_views.PasswordResetDoneView.as_view(
      template_name='accounts/authentications/password_reset_sent.html'
    ), name='password_reset_done'
  ),

  path('reset-password-complete/',
    auth_views.PasswordResetCompleteView.as_view(
      template_name='accounts/authentications/password_reset_complete.html'), name='password_reset_complete'
  ),
]