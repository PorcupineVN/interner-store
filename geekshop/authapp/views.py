from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from utils import send_verify_mail
from django.conf import settings
from .models import ShopUser
from django.db import transaction
from authapp.forms import ShopUserProfileEditForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(request, username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.GET.keys():
                    return HttpResponseRedirect(request.GET["next"])
                return HttpResponseRedirect(reverse('main'))
    else:
         login_form = ShopUserLoginForm()

    return render(request, 'authapp/login.html', context={
        'title': 'Вход в систему',
        'form': login_form
    })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            send_verify_mail(user)
            return HttpResponseRedirect(reverse('auth:login'))
    else:
       register_form = ShopUserRegisterForm() 

    return render(
        request, 
        "authapp/register.html", context={'title': 'Регистрация', 'form': register_form}
    )

@transaction.atomic
def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.profile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('main'))
    else:
       edit_form = ShopUserEditForm(instance=request.user)
       profile_form = ShopUserProfileEditForm(instance=request.user.profile)

    return render(
        request, 
        "authapp/edit.html", 
        context={"title": "Редактирование", "form": edit_form, "profile_form": profile_form},
    )

def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main'))