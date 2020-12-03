from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm, LoginForm, ProfileForm

from .models import User


def user_register(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['username']):
            return render(request, 'signup.html', {'existed_username': request.POST['username']})

        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
    return render(request, 'signup.html')


def user_login(request):
    invalid_login = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
            else:
                invalid_login = True
    return render(request, 'signin.html', {'invalid_login': invalid_login})


def user_logout(request):
    logout(request)
    return redirect('/login/')


def profile(request):
    user = User.objects.get(id=request.user.id)
    user_data = User.objects.filter(id=request.user.id).values(
        'first_name', 'last_name', 'avatar', 'birth_date', 'bio')[0]
    user_data['birth_date'] = user_data['birth_date'].strftime('%Y-%m-%d')

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm()

    return render(request, 'profile.html', {'user_data': user_data})
