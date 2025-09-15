
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include
from django.views.generic import RedirectView

import notice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/ad/profile', permanent=False), name='profile'),
    path('accounts/', include('allauth.urls')),
    path('pages', include('django.contrib.flatpages.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ad/', include('notice.urls')),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)