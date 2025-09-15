from django.utils.functional import empty
from django_filters import FilterSet, ModelChoiceFilter

from notice.models import Comment, Ad


class CommentFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop('request')
        self.filters['ad'].label = ''
        self.filters['ad'].queryset = Ad.objects.filter(user=self.user)


    ad = ModelChoiceFilter(queryset=Ad.objects.all(), label='Фильтр по объявлениям', empty_label='Все объявления')

