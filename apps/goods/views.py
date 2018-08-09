from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Goods, GoodsCategory, HotSearchWords, Banner
from .serializers import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializer, \
    IndexCategorySerializer
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework import viewsets

# from django_filter.rest_framework import DjangoFilterBackend

from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
from rest_framework import filters

from rest_framework.authentication import TokenAuthentication

#缓存，
from rest_framework_extensions.cache.mixins import CacheResponseMixin
#访问量，反爬虫
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
# Create your views here.

# class GoodsListView(APIView):
#     '''
#     list all goods
#     '''
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods, many=True)  #列表要加上many=True
#         return Response(goods_serializer.data)
#     def post(self, request, format=None):
#         serializer = GoodsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#     '''
#     商品列表页
#     '''
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

# 分页
class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'  # 将page 显示为p ,我们可以任意修改
    max_page_size = 100


# class GoodsListView(generics.ListAPIView):
#     '''
#     商品列表页
#     '''
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination


class GoodsListViewSets(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    trottle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication, )
    #           过滤           字段               搜索
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'shop_price')
    filter_class = GoodsFilter

    # 搜索字段
    search_fields = ('name', 'goods_brief', 'goods_desc')

    # 过滤
    ordering_fields = ('sold_num', 'shop_price')
    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     price_min = self.request.query_params.get('price_min', 0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     # return Goods.objects.filter(shop_price__gt=100)
    #     return queryset
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)




class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    '''

    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer

class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(viewsets.ModelViewSet):
    """
    首页商品分类数据
    """
    #
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer
