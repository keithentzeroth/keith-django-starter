from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms.util import ErrorList
from django.contrib.auth.models import User


@login_required
def home(request, extraStuff=None):
    return render_to_response('home.html', dict(), context_instance=RequestContext(request))



def vlogout(request):
    logout(request)
    form = LoginForm()
    return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))

def glogin(request):
    form = LoginForm()
    return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))

def plogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response('home.html', dict(), context_instance=RequestContext(request))
        else:
            form = LoginForm()
            return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))
    else:
        form = LoginForm()        
        return render_to_response('login.html',{'form':form} , context_instance=RequestContext(request))


def gaccount(request):
    form = SignUpForm(request.POST)
    return render_to_response('account/create.html',{'form':form}, context_instance=RequestContext(request))
    
def paccount(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email'].lower()
        firstname = form.cleaned_data['firstname'].capitalize()
        lastname = form.cleaned_data['lastname'].capitalize()
        # TODO: need to handle persistence errors for user, person and ticket!
        user = User.objects.create_user(form.cleaned_data['username'], email, form.cleaned_data['password'])
        # Disable the user until they've claimed their ticket
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        return render_to_response('account/created.html', dict(), context_instance=RequestContext(request))
    return render_to_response('account/create.html',{'form':form}, context_instance=RequestContext(request))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=75, min_length=5)
    password = forms.CharField(min_length=6, max_length=30, widget=forms.PasswordInput(render_value=False))
    next = forms.CharField(required=False,widget=forms.HiddenInput())
    
    
class SignUpForm(forms.Form):
    firstname = forms.CharField(max_length=40, min_length=2)
    lastname = forms.CharField(max_length=60, min_length=2)
    username = forms.CharField(max_length=75, min_length=5)
    email = forms.EmailField(max_length=75, min_length=5)
    password = forms.CharField(min_length=6,max_length=30,widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(min_length=6,max_length=30,widget=forms.PasswordInput(render_value=False))

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            msg = "Please enter the same password in each field."
            self._errors["password"] = ErrorList([msg])
            self._errors["password2"] = ErrorList([msg])
            # These fields are no longer valid. Remove them from the cleaned data.
            del cleaned_data["password"]
            del cleaned_data["password2"]
        return cleaned_data

