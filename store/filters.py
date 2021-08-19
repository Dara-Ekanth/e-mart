import django_filters
from .models import Product

class productfilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['image','description']



