from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView, DetailView, CreateView

from notice.forms import AdForm, CommentForm
from notice.models import Ad, UserCode

class Adlist(ListView):
    model = Ad
    context_object_name = 'ads'
    template_name = 'ad/ad_list.html'

class AdDetail(DetailView):
    model = Ad
    context_object_name = 'ad'
    template_name = 'ad/ad_detail.html'

    def post(self, request, *args, **kwargs):
        ad = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.ad = ad
            comment.save()
            send_mail(
                subject='Отклик на объявление',
                message=f'Привет {ad.user.username}!'
                        f'На ваше объявление "{ad.heading}" '
                        f'Пользователь: {comment.user.username} оставил отклик ',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[ad.user.email],

            )
            return redirect('ad_detail', ad.pk)
        return render(request, 'ad/ad_detail.html', {'form': form})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context




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
