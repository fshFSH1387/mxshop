import django_filters
from .models import Goods
from django.db.models import Q


#                               要有按钮需要添加rest_framework
class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品过滤器
    '''
    pricemix = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        #利用到外键，正向查询
        return queryset.filter(
            Q(category_id=value) |
            Q(category__parent_category_id=value) |
            Q(category__parent_category__parent_category_id=value)
        )

    class Meta:
        model = Goods
        fields = ['pricemix', 'pricemax', 'is_hot', 'is_new']
