"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from goods.views_base import GoodsListView
# from goods.views import GoodsListView
from users.views import SmsCodeViewset, UserViewset
# jwt认证
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSets, CategoryViewset, HotSearchsViewset, BannerViewset, IndexCategoryViewset
from rest_framework.routers import DefaultRouter
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from trade.views import ShoppingCartViewset, OrderViewset
from trade.views import AlipayView

router = DefaultRouter()

# 配置goods路由，以后配置只需要这样
router.register(r'goods', GoodsListViewSets, base_name='goods')
router.register(r'categorys', CategoryViewset, base_name='categorys')
router.register(r'code', SmsCodeViewset, base_name='code')
router.register(r'hotsearchs', HotSearchsViewset, base_name='hotsearchs')
router.register(r'users', UserViewset, base_name='users')

# 收藏
router.register(r'userfavs', UserFavViewset, base_name='userfavs')
# 留言
router.register(r'messages', LeavingMessageViewset, base_name='messages')
# 地址
router.register(r'address', AddressViewset, base_name='address')
# 订单
router.register(r'orders', OrderViewset, base_name='orders')

# 购物车
router.register(r'shopcarts', ShoppingCartViewset, base_name='shopcarts')

# 轮播图url
router.register(r'banners', BannerViewset, base_name="banners")

# 首页商品系列数据
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")

goods_list = GoodsListViewSets.as_view({
    'get': 'list',
})
from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    # drf登录配置
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),

    #     商品列表页面
    #     url(r'goods/$', GoodsListView.as_view(), name='goods-list'),
    #     url(r'goods/$', goods_list, name='goods-list'),
    # 支付宝付款后跳转页面
    url(r'^alipay/return/', AlipayView, name='alipay'),
    url(r'^index/', TemplateView.as_view(template_name='index.html'), name='index'),

    # 自动生成drf文档的配置
    url(r'^docs/', include_docs_urls(title='慕学生鲜')),
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证
    url(r'^login/$', obtain_jwt_token),
    url(r'^', include(router.urls)),
    url(r'', include('social_django.urls', namespace='social'))

]
