from django.urls import path

from .views import ad_detail, ConfirmUser, profile

urlpatterns = [
    path('<int:pk>', ad_detail ,name='ad_detail'),
    path('confirm_user/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', profile, name='profile'),
]