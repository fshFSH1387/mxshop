from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializers import UserFavDetailSerializer, LeacingMessageSerializer


# Create your views here.
class UserFavViewset(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    '''
    list:
        获取用户收藏列表
    retrieve：
        判断某个商品是否收藏
    create：
        收藏商品

    '''
    # queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

    def perform_destroy(self, instance):
        # instance = instance.delete()
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer


# 留言
class LeavingMessageViewset(mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    '''
    list:
        获取用户留言
    delete:
        删除用户留言
    create:
        创建用户留言
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeacingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    '''
    收货地址管理
    list:
        获取收货地址
    delete:
        删除收货地址
    create：
        创建收货地址
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = AddressSerializer
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
