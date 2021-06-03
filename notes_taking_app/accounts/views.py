from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from .forms import LoginForm, SignUpForm
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
      return HttpResponse('<h1> Welcome to homepage </h1>')

  template_name = 'accounts/authentications/login.html'
  context = {'form': form}
  return render(request, template_name, context)

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

def check_username_validity(request):
  if request.is_ajax and request.method == 'POST':
    if Account.objects.filter(username=request.POST['username']).exists():
      return JsonResponse({'message': 'Username already taken', 'class': 'danger'})
    return JsonResponse({'message': 'Username available', 'class': 'success'})