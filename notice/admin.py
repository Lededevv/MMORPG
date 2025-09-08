from django.contrib import admin

from notice.models import Ad, Category, Comment

admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Comment)