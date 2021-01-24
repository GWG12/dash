from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib import messages
import mercadopago
import json


'''class LoginViewCustom(LoginView):
    #esport_user = EsportUser.objects.first()
    #extra_context = {'test42': esport_user}
    template_name = 'dashboard-login.html'
    authentication_form = LoginForm'''

#openpay



def test(request):
    form = LoginForm()
    return render(request,'dashboard-crm.html',{'form':form})

def home(request):
    print(request.user)
    return render(request,'index.html')

def login(request):
    #LoginForm
    print("Paso a TESTING")
    if request.method == 'POST':
        email = request.POST.get('mail')
        password = request.POST.get('password')
        print('Justo antes de AUTH')
        user = authenticate(username=email,password=password)

        print('AFTER AUTH', request.user)
        if user is not None:
            if user.is_active:
                #Esto es lo que guarda al usuario en la sesión y corre la función de get_user del backend
                auth_login(request,user)
                return redirect('home')
    else:
        form = LoginForm()
        return render(request,'dashboard-login.html',{'form':form})

def register(request):
    if request.method == 'POST':
        print('EL POST')
        form = UserRegistrationForm(request.POST)
        print(request.POST)
        print("VALIDACION ", form.is_valid())
        print("los errores ", form.errors)
        if form.is_valid():
            print("Es valido")
            email = form.cleaned_data.get('email')
            print(email, type(email))
            #form.save()
            instance = form.save(commit=False)
            user = email.split('@')
            user_second_part = user[1].split('.')[0]

            final_user = user[0] + '_' + user_second_part
            print("Nombre de usuario ",final_user)
            instance.username = final_user
            instance.save()
            #messages.success(request,f'Account created for {email}!')
            return redirect('login')
        print("PWEWENGREONEIH")
    else:
        form = UserRegistrationForm()
    return render(request,'dashboard-register.html',{'form':form})
