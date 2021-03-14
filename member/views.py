from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Alfaaz import settings
from member.models import Member
from member.forms import UserForm, RegistrationForm, LoginForm, ContactForm

# Create your views here.

def home(request): # the function will take request as input
    return render(request, 'member/home.html') # the function then renders an html page template called home.html

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "ALFAAZ INQUIRY"
            body = {
                'contact_name': form.cleaned_data['contact_name'],
                'contact_email': form.cleaned_data['contact_email'],
                'content': form.cleaned_data['content'],
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, ['avibilasgupta@gmail.com'], fail_silently=False  )
            except BadHeaderError:
                return HttpResponse('Invalid Header Found')
            return HttpResponseRedirect(reverse('home'))
    form = ContactForm()
    return render(request, 'member/contact.html', {'form':form})

def about_view(request):
    return render(request, 'member/about.html')

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
        return render(request, 'member/login.html', {})


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

@login_required
def profile(request):
    if request.method=='GET':
        enrollment_number = request.GET.get('enrollment_number')
        member_info = Member.objects.filter(enrollment_number = enrollment_number)
        return render(request, 'member/profile.html',{'member_info':member_info})