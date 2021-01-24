from django.urls import path
from amazon import views as amazon_views

urlpatterns = [
    path('upload/',amazon_views.image_upload,name='upload'),
    ]
