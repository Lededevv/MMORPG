from django.urls import path

from .views import AdDetail, ConfirmUser, Adlist, AdCreate, Profile, comment_accept, comment_reject

urlpatterns = [
    path('', Adlist.as_view(), name='ad_list'),
    path('<int:pk>', AdDetail.as_view() ,name='ad_detail'),
    path('confirm_user/', ConfirmUser.as_view(), name='confirm_user'),
    path('create/', AdCreate.as_view(), name='create'),
    path('profile/', Profile.as_view(), name='profile'),
    path('comment/<int:pk>/accept', comment_accept, name='comment_accept'),
    path('comment/<int:pk>/reject', comment_reject, name='comment_reject'),

]