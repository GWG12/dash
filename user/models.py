from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    #user = models.OneToOneField(User, related_name="user_profile",null=True, blank=True,on_delete=models.CASCADE)
    #user = models.OneToOneField(User,on_delete=models.CASCADE)
    user = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    openpay_customer_id = models.CharField(max_length=100,blank=True)
    project_name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.name} Profile'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    #instance.profile.save()

class Cards(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    openpay_card_id = models.CharField(max_length=30)


    def __str__(self):
        return f'{self.profile} Card'

# Create your models here.
