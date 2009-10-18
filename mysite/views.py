from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from mysite.polls.models import Poll
from django import forms

def home_view(request, extraStuff=None):
    if request.user.is_authenticated():
        print('user is authorized')
        return render_to_response('loggedin.html', dict())
    else:
        form = LoginForm()
        return render_to_response('login.html', {'form':form})


def logout_view(request):
    logout(request)
    form = LoginForm()
    return render_to_response('login.html', {'form':form})

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response('loggedin.html', dict())
        else:
            form = LoginForm()
            return render_to_response('login.html', {'form':form})
    else:
        form = LoginForm()        
        return render_to_response('login.html',{'form':form} )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=75, min_length=5)
    password = forms.CharField(min_length=6, max_length=30, widget=forms.PasswordInput(render_value=False))
    next = forms.CharField(required=False,widget=forms.HiddenInput())
