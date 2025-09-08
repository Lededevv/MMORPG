from django.urls import path

from .views import ad_detail

urlpatterns = [
    path('<int:pk>', ad_detail ,name='ad_detail'),

]