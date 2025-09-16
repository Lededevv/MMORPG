from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView, DetailView, CreateView
from notice.filters import CommentFilter
from notice.forms import AdForm, CommentForm
from notice.models import Ad, UserCode, Comment


class Adlist(ListView):
    ordering = '-time_in'
    model = Ad
    context_object_name = 'ads'
    template_name = 'ad/ad_list.html'
    paginate_by = 5

class AdEdit(LoginRequiredMixin, UpdateView):

    form_class = AdForm
    model = Ad
    template_name = 'ad/ad_edit.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

class AdDetail(LoginRequiredMixin,DetailView):
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



class Profile(LoginRequiredMixin, ListView):

    model = Comment
    context_object_name = 'comments'
    template_name = 'ad/profile.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(ad__user=self.request.user)
        self.filter = CommentFilter(self.request.GET, queryset, request=self.request.user)
        return self.filter.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        return context

def comment_accept(request,pk):
    comment = Comment.objects.get(pk=pk)
    comment.status = 'accept'
    comment.save()

    send_mail(
                    subject='Принятие отклика',
                    message='Ваш отклик был принят',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[comment.user.email],

                )
    return redirect(request.META.get("HTTP_REFERER"))

def comment_reject(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.status = 'reject'
    comment.save()
    return redirect(request.META.get("HTTP_REFERER"))