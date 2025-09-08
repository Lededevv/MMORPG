from django.shortcuts import render

from notice.models import Ad


def ad_detail(request, pk):
    ad = Ad.objects.get(pk=pk)
    return render(request, 'ad/ad_detail.html', {'ad':ad})
