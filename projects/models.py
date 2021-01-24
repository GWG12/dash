from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Projects(models.Model):

    WEB = 'W'
    BRANDING = 'B'
    CATEGORIES = (
        (WEB, (('custom','Personalizada'),('template','Plantilla'))),
        (BRANDING, 'Branding'),)
    BASIC = "BAS"
    PRO = "PRO"
    VIP = "VIP"
    PACKAGES = ((BASIC,'Basic'),(PRO,'Pro'),(VIP,"Vip"),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20,choices=CATEGORIES)
    package = models.CharField(max_length=3,choices=PACKAGES)
    description = models.TextField()
    payment = models.FloatField()
    total_cost = models.FloatField()
    date_posted = models.DateTimeField(default=timezone.now)
    delivery_date = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.project_name} Proyecto'
