from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.http import HttpResponse, JsonResponse, Http404
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import LoginForm, SignUpForm, ProfileUpdateForm
from .models import Account

def login_view(request):
  form = LoginForm()
  
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(username=username, password=password)
      login(request, user)
      return redirect('accounts:home_page')

  template_name = 'accounts/login.html'
  context = {'form': form}
  return render(request, template_name, context)

def logout_view(request):
  logout(request)
  return redirect('accounts:login')  

def signup_view(request):
  form = SignUpForm()
  
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      new_user = form.save(commit=False)
      new_user.set_password(form.cleaned_data['re_password'])
      new_user.save()
      return redirect('accounts:login')

  template_name = 'accounts/authentications/signup.html'  
  context = {'form': form}
  return render(request, template_name, context)

def profile_update_view(request):
  if request.user.is_authenticated:
    form = ProfileUpdateForm(
      request.POST or None, 
      request.FILES or None, 
      instance=request.user 
    )
    
    if form.is_valid():
      form.save()
      return redirect('accounts:home_page') 

  template_name = 'accounts/authentications/profile_form.html'
  context = {'form': form}    
  return render(request, template_name, context)

def check_username_validity(request):
  if request.is_ajax and request.method == 'POST':
    if Account.objects.filter(username=request.POST['username']).exists():
      return JsonResponse({'message': 'Username already taken', 'class': 'danger'})
    return JsonResponse({'message': 'Username available', 'class': 'success'})

def password_change_view(request):
  form = PasswordChangeForm(request.user)
  if request.method == 'POST':
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      form.save()
      logout(request)
      return redirect('accounts:login')

  template_name = 'accounts/authentications/password_change_form.html'
  context = {'form': form}
  return render(request, template_name, context)

def password_reset_view(request):
  form = PasswordResetForm()

  if request.method == 'POST':
    form = PasswordResetForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data.get('email')

      try:
        user = Account.objects.get(email=email)
        subject = 'Password Reset Requested'
        email_template_name = 'accounts/authentications/password_reset_email.txt'

        email_context = {
          "email": user.email,
          "domain": "127.0.0.1:8000",
          "site_name": "Super Notes",
          "uid": urlsafe_base64_encode(force_bytes(user.pk)),
          "user": user,
          "token": default_token_generator.make_token(user),
          "protocol": "http"
        }
        email_message = render_to_string(email_template_name, email_context)

        try:
          send_mail(subject, email_message, 'nimra.rahim99@gmail.com', [user.email], fail_silently=False)
        except BadHeaderError:
          HttpResponse("Invalid Header found.")

      except Account.DoesNotExist:
        raise Http404('No Such account with this email address.')
      return redirect('accounts:password_reset_done')

  template_name = 'accounts/authentications/password_reset.html'
  context = {'form': form}
  return render(request, template_name, context) 

#Overriding built-in auth view
class PasswordResetConfirmView(PasswordResetConfirmView):
  success_url = reverse_lazy('accounts:password_reset_complete')
  template_name='accounts/authentications/password_reset_confirm.html'
  

def home_view(request):
  return render(request, 'accounts/home.html')    

