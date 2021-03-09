from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from member.models import Member
from member.forms import UserForm, RegistrationForm, LoginForm

# Create your views here.

def home(request): # the function will take request as input
    return render(request, 'home.html') # the function then renders an html page template called home.html


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        registration_form = RegistrationForm(data=request.POST)
        if user_form.is_valid() and RegistrationForm.is_valid():
            new_member = user_form.save()
            fss = FileSystemStorage()
            new_member.set_password(new_member.password)
            new_member.save()
            member_registration = registration_form.save(commit=False)
            member_registration.user =new_member
            member_registration.save()
            registered = True
        else:
            print(user_form.errors, registration_form.errors)
    else:
        user_form = UserForm()
        registration_form = RegistrationForm()
    return render(request, 'reg_form.html',
                            {'user_form': user_form,
                            'registration_form': registration_form,
                            'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                member = Member.objects.get(user__username=username)
                return render(request, 'profile.html', {"user": user})
            else:
                return HttpResponse('Disabled account')
        else:
                return HttpResponse('Invalid Login')
    else:
        return render(request, 'login.html', {})


@login_required
def edit(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=request.user.member)
        if form.is_valid():
            form.save()
            return render(request, 'profile.html')
    else:
        form = RegistrationForm(instance=request.user.member)
        return render(request, 'edit.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))