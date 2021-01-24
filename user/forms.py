from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm



class LoginForm(AuthenticationForm):
    mail = forms.CharField(widget=forms.EmailInput(
    attrs={
        'class': 'input is-large',
        'placeholder': 'E-mail'
    }))
    password = forms.CharField(widget=forms.PasswordInput(
    attrs={
        'class': 'input is-large',
        'placeholder': 'Contraseña'
    }))

    '''def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)'''

    '''def get_user(self):
        print('get user AUTHENTICATE')
        return None'''

class UserRegistrationForm(UserCreationForm):



    email = forms.CharField(widget=forms.EmailInput(
    attrs={
        'class': 'input is-large',
        'placeholder': 'E-mail'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(
    attrs={
        'class': 'input is-large',
        'placeholder': 'Contraseña'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(
    attrs={
        'class': 'input is-large',
        'placeholder': 'Comprueba tu contraseña'
    }),
    error_messages={'invalid': 'Las dos contraseñas son diferentes, vuelve a ingresar la contraseña.'})

    class Meta:
        model=User
        fields = ('email','password1', 'password2')
        #exclude = ('username',)

    def clean_email(self):
        print('email')
        email = self.cleaned_data.get('email')
        print('previo a checking email ',email)
        mail_checked = User.objects.filter(email = email)
        print("mail checked ",mail_checked)
        if mail_checked:
            print('verdadero')
            raise forms.ValidationError('Ya existe el correo')
        else:
            print('falso')
            return email

    '''def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'input is-large'
        self.fields['password1'].widget.attrs['class'] = 'input is-large'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['class'] = 'input is-large'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repite contraseña'''


    def clean_password2(self):
        print("cleaning the data")
        #cleaned_data = super(UserRegistrationForm, self).clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        print("CLEAN")
        #user_qs = User.objects.filter(username=username)
        #if user_qs.count() == 1:
        #   user = user_qs.first()
        if password1 != password2:
            print(password1, password2)
            raise forms.ValidationError("Las contraseñas son diferentes")
            print('post raise error contraseña')
