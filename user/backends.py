from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class EmailBackend(ModelBackend):

    def authenticate(self,request,username=None,password=None,**kwargs):
        print('authenticate function')
        try:
            print(username,password)
            user = User.objects.get(email=username)
            print("EL USUARIO ", user)
        except User.MultipleObjectsReturned:
            user = User.objects.filter(email=username).order_by('id').first()
        except User.DoesNotExist:
            return None

        if getattr(user,'is_active') and user.check_password(password):
            print('authenticate user ', user)
            return user
        return None


    def get_user(self,user_id):
        print('get user AUTHENTICATE',user_id)
        try:
            print("Try de get_user")
            print('Usuario ', User.objects.get(pk=user_id))
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            print("NO PASO")
            return None
