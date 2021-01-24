# Jaqlap

Ecommerce for websites. Status: unfinished

# Guía de Uso

Se cuentan con las siguientes rutas:

## Login

*/login*

## Password Reset
*/password-reset*

## Projects

*/projects*

Campos sin modificar desde primera iteración del desarrollo

## Openpay

La siguiente view, localizada en:
``` python
openpay_shop.views
```
registra el cliente en db y openpay, realiza el pago, registra la tarjeta en openpay y genera la suscripción:


```python
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

        if form_user.is_valid() and form_profile.is_valid():
            #openpay settings
            openpay.verify_ssl_certs = False
            openpay.api_key = "xxxxxxxxxxxx"
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
                'plan_id': 'p5r3vhg1akacdcnp0e9g',
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
```
#### Pasos para usar app Openpay:
1. Entrar a **/openpay/planes** y selecciona el plan deseado. Redirecciona a ruta **/openpay/registro-cliente/<plan>**

2. Llenar la información solicitada en la forma. Para los datos de tarjeta: colocar los sig:
  - **#Tarjeta**: xxxxxxxxxxxxxxxx
  - **Mes**: xx
  - **Año**: xx
  - **cvc**: xxx  

3. Verificar en dashboard de openpay que el cliente y suscripción hayan sido creados.


## Amazon S3
Guarda archivos en bucket S3.

Plantilla HTML: **dashkit/amazon/upload.html**

Ruta en broswer: **amazon/upload**

Para restringir cierto tipo de archivos, se implementó la siguiente función (solo funciona para archivos .zip, aunque se probó con archivos individuales y si funcionó):

```python
def clean_image(self):

    supported_types=['jpg',] #only accepts .jpg extensions
    files = self.cleaned_data['image'] #uploaded file
    zip = zipfile.ZipFile(files)
    print(zip.namelist())
    for file in zip.namelist(): #lists all files in .zip folder
        print(file.split('.')[1].lower())
        if not file.split('.')[1].lower() in supported_types:
            raise forms.ValidationError('Solo se permiten archivos jpg') #Displays this error in HTML template in case file extension is not allowed
    return files
```
###### Consideraciones
Este tipo de validación solo revisa la extensión, mas no revisa el tipo de archivo (MIME type). Alguien podría subir un archivo incorrecto agregando la extensión aceptada al final. La solución es usar la librería, pero tuve un error en la importación.


## Plantillas de Login HTML


**Login**: *dashkit\dashboard-login.html*

**Registro de Nuevo Usuario**: *dashkit\dashboard-register.html*

**Reset Password** = (Todas las rutas que empiezan con password)

**NOTA**
*Hay que definir un base.html para todas las plantillas que tengamos que usar.
