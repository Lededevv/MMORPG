from allauth.account.forms import SignupForm

from django.core.mail import send_mail

from MMORPG import settings
from notice.models import UserCode
import secrets


class ConfirmSignupForm(SignupForm):

    def save(self, request):
        user = super().save(request)
        user.is_active = False
        user.save()
        code = secrets.token_urlsafe(10)
        UserCode.objects.create(user=user , code=code)

        send_mail(
            subject='Активация аккаунта',
            message=f"Привет, {user.username}! Активируй свой аккаунт"
                    f"по коду {code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )

        return user