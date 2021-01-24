from django.shortcuts import render, redirect
from django.http import HttpResponse
import openpay
import json
from .forms import SubscriptionRegistrationForm
from user.forms import UserRegistrationForm
from user.models import Cards


openpay.api_key = "xxxxxx"
openpay.verify_ssl_certs = False
openpay.merchant_id = "xxxxxx"


def planes(request):
    return render(request,'openpay_templates/planes.html')

def registro_cliente(request,plan):
    print("El plan ", plan)
    #Openpay credentials for generating token in Front End
    data = {
    'credentials': {
            'api_key': openpay.api_key,
            'shop_id': openpay.merchant_id
        }
    }
    #plan = subscription type,
    context = {
        'plan':plan,
        'data':data
    }
    if request.method == 'POST':
        print("Forma subida ",request.POST)
        form_user = UserRegistrationForm(request.POST)
        form_profile = SubscriptionRegistrationForm(request.POST)
        print("TOKEN ",request.POST.get('token_id'))
        '''if form_user.is_valid() and form_profile.is_valid():
            email = form_user.cleaned_data.get('email')
            instance = form_user.save(commit=False)
            user = email.split('@')
            user_second_part = user[1].split('.')[0]
            final_user = user[0] + '_' + user_second_part
            instance.username = final_user
            instance.save()
            form_profile.save(commit=False)
            print("INSTANCIA ",instance, type(instance))
            print("NOMBRE DE USUARIO ",instance.username, )
            form_profile.user = instance
            print("FORMA Profule ",form_profile, type(form_profile))
            form_profile.save()
            redirect('mercado')'''

        if form_user.is_valid() and form_profile.is_valid():
            #openpay settings
            openpay.verify_ssl_certs = False
            openpay.api_key = "xxxxxx"
            #Saving to User
            email = form_user.cleaned_data.get('email')
            instance = form_user.save(commit=False)
            #Creates custom username from email name and domain
            user = email.split('@')
            user_second_part = user[1].split('.')[0]
            final_user = user[0] + '_' + user_second_part
            instance.username = final_user
            instance.save()
            #Saving customer to Openpay
            new_user_payload = {
                'name':form_profile.cleaned_data.get('name'),
                'email': form_user.cleaned_data.get('email')
            }
            customer = openpay.Customer.create(**new_user_payload)
            print("CLIENTE Openpay ",customer)
            #Saving to Profile
            instance.profile.name = form_profile.cleaned_data.get('name')
            instance.profile.project_name = form_profile.cleaned_data.get('project_name')
            instance.profile.openpay_customer_id = customer['id']
            instance.profile.save()
            #Saving card and bind it to recent user in Openpay
            payload_card = {
                'token_id':request.POST.get('token_id'),
                'device_session_id': request.POST.get('deviceIdHiddenFieldName')
            }
            card = customer.cards.create(**payload_card)
            print("TARJETA Openpay ",card)
            #Saves new card to Cards Model
            new_card = Cards(profile=instance.profile,openpay_card_id=card['id'])
            new_card.save()
            #Creates customer's subscription
            #plan_id is hard coded, it should be dynamic in later implementations
            payload_subscription = {
                'plan_id': 'xxxxxx',
                'card_id': card['id']
            }
            #para comprobar que la suscripcion fue exitosa,  se pueden obtener los sigs. campos del objeto
            #subscription: id & status
            pago = customer.subscriptions.create(**payload_subscription)
            print("Suscripcion ", pago)
            return redirect('mercado')
        context['form_user'] = form_user
        context['form_profile'] = form_profile
    else:
        form_user = UserRegistrationForm()
        form_profile = SubscriptionRegistrationForm()
        context['form_user'] = form_user
        context['form_profile'] = form_profile

    return render(request,'openpay_templates/registro-cliente.html',context)

def nuevo_cliente(request):
    payload = {
        'name':'Roberto',
        'email': 'roberto@gmail.com'
    }
    openpay.verify_ssl_certs = False
    openpay.api_key = "xxxxxx"
    customer = openpay.Customer.create(**payload)
    print(customer)
    return HttpResponse('<h1>Se inscribio</h1>')

def suscripcion(request):
    data = {
    'credentials': {
            'api_key': openpay.api_key,
            'shop_id': openpay.merchant_id
        }
    }
    if request.method == 'POST':
        openpay.verify_ssl_certs = False
        openpay.api_key = "xxxxxx"
        print("TOKEN ",request.POST.get('token_id'))
        print("DEVICE ",request.POST.get('deviceIdHiddenFieldName'))
        payload_card = {
            'token_id':request.POST.get('token_id'),
            'device_session_id': request.POST.get('deviceIdHiddenFieldName')
        }
        customer = openpay.Customer.retrieve('xxxxxx')
        print("Cliente ",customer)
        card = customer.cards.create(**payload_card)
        print("Tarjeta ",type(card), card)
        payload_subscription = {
            'plan_id': 'xxxxxx',
            'card_id': card['id']
        }
        pago = customer.subscriptions.create(**payload_subscription)
        print("Suscripcion ", pago)
        return redirect('mercado')
    return render(request,'openpay_templates/suscripcion.html',{'data':data})

def compra(request):
    data = {
    'credentials': {
            'api_key': openpay.api_key,
            'shop_id': openpay.merchant_id
        }
    }
    if request.method == 'POST':
        openpay.verify_ssl_certs = False
        openpay.api_key = "xxxxxx"
        print("TOKEN ",request.POST.get('token_id'))
        print("DEVICE ",request.POST.get('deviceIdHiddenFieldName'))
        payload = {
            'method': 'card',
            'source_id': request.POST.get('token_id'),
            'amount':10.00,
            'description':'Producto de prueba',
            'device_session_id': request.POST.get('deviceIdHiddenFieldName')
        }
        customer = openpay.Customer.retrieve('xxxxxx')
        print("Cliente ",customer)
        pago = customer.charges.create(**payload)
        print(pago)
        return redirect('mercado')
    return render(request,'openpay_templates/card_form/card.html',{'data':data})
