from django.shortcuts import render, redirect
import mercadopago
import json


PUBLIC_KEY = 'xxxxxx'
ACCESS_TOKEN = 'xxxxxx'
CLIENT_ID = 'xxxxxx'
CLIENT_SECRET = 'xxxxxx'


def mercado(request):


    return render(request,'mercado_pago/mercado.html')

def suscripcion(request):
    mp = mercadopago.MP(ACCESS_TOKEN)
    if request.method == "POST":
        pass
    cliente = mp.get('/v1/customers/search',{'email': 'test2@gmail.com'})
    id_cliente = cliente['response']['results'][0]['id']
    tarjetas = mp.get('/v1/customers/' + id_cliente + '/cards')
    print("TARJETAS ",json.dumps(tarjetas,indent=4))
    tarjeta_id = tarjetas['response'][0]['id']
    token = mp.post('/v1/card_tokens',{'card_id':tarjeta_id})
    token_number = token['response']['id']
    print("TOKEN ", token_number)
    print("ID CLIENTE ", id_cliente)
    payment_data = {
            'transaction_amount': 100,
            'token': token_number,
            'installments':1,
            'payer':{
                'id': id_cliente,
            }
        }
    pago = mp.post("/v1/payments", payment_data)
    print("PAGO ", json.dumps(pago,indent=4))
    return render(request,'mercado_pago/suscripciones.html')

def ver_clientes(request):
    mp = mercadopago.MP(ACCESS_TOKEN)
    if request.method == "POST":
        print("TOKEN Tarjeta ",request.POST.get('token'))
        payment_data = {
            'transaction_amount': 100,
            'token': request.POST.get('token'),
            'installments':1,
            'payer':{
                'id': 'xxxxxx',
                'type': 'customer'
            },
            'currency_id': 'MXN',
            'frequency_type':'months',
            'frequency':1
        }
        pago = mp.post("/v1/payments", payment_data)
        print("JSON del Pago ",json.dumps(pago,indent=4))
        return redirect('mercado')
    cliente = mp.get('/v1/customers/search',{'email': 'test2@gmail.com'})
    print("ID Tarjeta ",cliente['response']['results'][0]['cards'][0]['id'])
    data = {'card_id':cliente['response']['results'][0]['cards'][0]['id']}
    return render(request,'mercado_pago/pago.html',{'data':data})


def crear_cliente(request):
    mp = mercadopago.MP(ACCESS_TOKEN)
    if request.method == 'POST':
        '''params = {
            'transaction_amount': request.POST.get('transaction_amount'),
            'token': request.POST.get('token'),
            'description': request.POST.get('description'),
            'payment_method_id': request.POST.get('payment_method_id'),
            'description': request.POST.get('description'),
            'payer': {
            'email': request.POST.get('email')
            }
        }'''
        email = request.POST.get('email')
        cliente = mp.post("/v1/customers", {"email": email})
        print(json.dumps(cliente,indent=4))
        #clienteNew = json.loads(cliente)
        token = request.POST.get('token')
        tarjeta = mp.post("/v1/customers/" + cliente['response']['id'] + '/cards', {"token": token})
        print(json.dumps(tarjeta,indent=4))
        print(token)
        print('NO')

        return redirect('mercado')
    return render(request,'mercado_pago/cliente.html')
