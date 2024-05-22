import django_filters
from django_filters import CharFilter

from models import Manager


class ManagerFilter(django_filters.FilterSet):

    class Meta:
        model = Manager
        fields = ['display_name']