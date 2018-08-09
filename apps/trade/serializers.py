from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer

import time
from random import Random

from MxShop.settings import private_key_path, alipay_pub_key_path
from utils.alipay import AliPay


# class ShopCartSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#     add_time = serializers.DateTimeField(read_only=True)
#
#     class Meta:
#         model = ShoppingCart
#         fields = ('user', 'goods', 'nums', 'add_time')

class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    })

    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(),
                                               required=True)

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    '''
    `update()` must be implemented.
    用到serializer 里面的方法需要重写
    '''

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        # fields = ("goods", "nums")
        fields ="__all__"


class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)


    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerialzier(many=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)
    def get_alipay_url(self, obj):
        '''
        支付宝url
        :param object:
        :return:
        '''
        alipay = AliPay(
            appid="2016091600527101",
            app_notify_url="http://211.159.158.158:8001/alipay/return/",
            app_private_key_path=private_key_path, #支付公钥
            alipay_public_key_path=alipay_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # debug=True,  # 默认False,
            return_url="http://211.159.158.158:8001/alipay/return/"
        )
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            return_url="http://211.159.189.158:8001"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        # print(re_url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        '''
        支付宝url
        :param object:
        :return:
        '''
        alipay = AliPay(
            appid="2016091600527101",
            app_notify_url="http://211.159.158.158:8001/alipay/return/",
            app_private_key_path=private_key_path, #支付公钥
            alipay_public_key_path=alipay_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # debug=True,  # 默认False,
            return_url="http://211.159.158.158:8001/alipay/return/"
        )
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            return_url="http://211.159.189.158:8001"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        # print(re_url)
        return re_url



    def generate_order_sn(self):
        random_ins = Random()

        order_sn = '{time_str}{userid}{ranstr}'.format(time_str=time.strftime('%Y%m%d%H%M%S'),
                                                       userid=self.context['request'].user.id,
                                                       ranstr=random_ins.randint(100000, 999999))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'

'''
9e:c6:d7:ba:b3:02:cd:07:d3:47:1e:47:22:5a:2f:b2
'''
