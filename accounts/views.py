from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm


def user_login(request):
    invalid_login = False
    if request.method == 'POST':
        print("2", flush=True)
        form = LoginForm(request.POST)
        if form.is_valid():
            print("3", flush=True)
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    print("4", flush=True)
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('Disabled account')
            else:
                invalid_login = True
    else:
        form = LoginForm()
    return render(request, 'signin.html', {'invalid_login': invalid_login})

def user_logout(request):
    logout(request)
    return redirect('/login/')
