from django.shortcuts import render
from django.contrib import auth, messages
from django.http import  HttpResponseRedirect

from django.urls import reverse

from locations.models import Location
from users.forms import UserLoginForm, UserRegistrationForm, UserSettingsForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserLoginForm()
    context = {'form' : form}
    return render(request, 'users/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered ✅')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'users/registration.html', context)

def profile(request):
    user = request.user
    locations = Location.objects.filter(user_id=user.id)
    print(type(user))
    if user.is_active:
        context = {'user' : user, 'locations' : locations}
        return render(request, 'users/profile.html', context)
    else:
        return HttpResponseRedirect(reverse('users:login'))


def settings(request):
    if request.method == 'POST':
        form = UserSettingsForm(instance=request.user, data=request.POST)
        print("Est")
        if form.is_valid():
            print("Valid")
            form.save()
            return HttpResponseRedirect(reverse('users:settings'))
        else:
            print(form.errors)
    else:
        form = UserSettingsForm(instance=request.user)
    context = {'form' : form}
    return render(request, 'users/settings.html', context)
