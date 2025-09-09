from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from notice.models import Ad, UserCode


def ad_detail(request, pk):
    ad = Ad.objects.get(pk=pk)
    return render(request, 'ad/ad_detail.html', {'ad':ad})

class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'user'

    def post(self,request, *args, **kwargs):
        if 'code' in request.POST:
            code = request.POST['code']
            user_code = UserCode.objects.filter(code=code)
            if user_code.exists():
                user_code.user.is_active = True
                user_code.user.save()
        return redirect('account_login')
