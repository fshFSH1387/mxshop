from rest_framework import serializers

# from settings import REGEX_MOBILE
import re
from datetime import datetime, timedelta

from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param data:mobile
        :return:mobile
        '''
        # 存在
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')
        # 合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码非法')

        # 验证码发送频率
        one_mintes_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_age, mobile=mobile).count():
            raise serializers.ValidationError('距离上次发送验证码没超过60s')

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户详情序列化
    '''

    class Meta:
        model = User
        fields = ('name', 'gender', 'birthday', 'email', 'mobile')


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4,
                                 min_length=4,
                                 label='验证码',
                                 write_only=True,  # 有他就不会序列化了
                                 required=True,
                                 help_text='验证码',
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 )

    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message='用户已经存在')],
                                     label='用户',
                                     help_text='用户名')
    password = serializers.CharField(
        style={'input_type': 'password'},
        label='密码',
        write_only=True,
        help_text='密码'
    )
    #设置密码加密
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            # 一定要注意时间的转换 timezone
            five_mintes_ago = timezone.now() - timedelta(hours=0, minutes=5, seconds=0)
            # five_mintes_ago.astimezone(timezone.utc).replace(tzinfo=None)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')
