from django.contrib import admin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from MMORPG import settings
from notice.models import Ad, Category, Comment, News

admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Comment)


def send_news(modeladmin, request, queryset):
    for news_one in queryset:
        subject = news_one.title
        message = news_one.content
        users_emails = [user.email for user in User.objects.all()]
        print(users_emails)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = users_emails  # Замените на список получателей
        send_mail(subject, message, from_email, recipient_list)
    redirect(request.META.get("HTTP_REFERER"))  # Перенаправление на список новостей

@admin.register(News)
class News(admin.ModelAdmin):
    actions = [send_news]

send_news.short_description = 'отправить рассылку по выбранной новости'
