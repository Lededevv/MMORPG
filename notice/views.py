from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView, DetailView, CreateView

from notice.forms import AdForm
from notice.models import Ad, UserCode

class Adlist(ListView):
    model = Ad
    context_object_name = 'ads'
    template_name = 'ad/ad_list.html'

class AdDetail(DetailView):
    model = Ad
    context_object_name = 'ad'
    template_name = 'ad/ad_detail.html'

class AdCreate(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ad/ad_create.html'
    login_url = 'account_login'

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.user = self.request.user
        ad.save()
        return super().form_valid(form)




class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'user'

    def post(self,request, *args, **kwargs):

        if 'code' in request.POST:
            code = request.POST['code']
            user_code = UserCode.objects.filter(code=code)
            if user_code.exists():
                user = UserCode.objects.get(code=code).user
                user.is_active = True
                user.save()
                user_code.update(code=None)
            else:
                return render(request,'ad/code_error.html', {'code': code})

        return redirect('account_login')


@login_required
def profile(request):
    return render(request, 'ad/profile.html')
