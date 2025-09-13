from django.urls import path

from .views import AdDetail, ConfirmUser, profile, Adlist, AdCreate

urlpatterns = [
    path('', Adlist.as_view(), name='ad_list'),
    path('<int:pk>', AdDetail.as_view() ,name='ad_detail'),
    path('confirm_user/', ConfirmUser.as_view(), name='confirm_user'),
    path('create/', AdCreate.as_view(), name='create'),
    path('profile/', profile, name='profile'),

]