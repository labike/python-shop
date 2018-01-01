"""shops URL Configuration

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
# from django.contrib import admin
import xadmin
from shops.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from django.views.generic import TemplateView

from goods.views import GoodsListViewSet, CategoryViewSet, HotSearchViewSet, BannerViewSet
from goods.views import IndexCategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet, AliPayView

router = DefaultRouter()

#goods--->url
router.register(r'goods', GoodsListViewSet, base_name='goods')

#code--->url
router.register(r'code', SmsCodeViewSet, base_name='code')

#hotwords--->url
router.register(r'hotsearchs', HotSearchViewSet, base_name="hotsearchs")

#user--->url
router.register(r'users', UserViewSet, base_name='users')

#user--->url
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')

#category--->url
router.register(r'categorys', CategoryViewSet, base_name='categorys')

#slider image--->url
router.register(r'banners', BannerViewSet, base_name="banners")

#index goods data--->url
router.register(r'indexgoods', IndexCategoryViewSet, base_name="indexgoods")

#leaving message--->url
router.register(r'messages', LeavingMessageViewSet, base_name="messages")

#address--->url
router.register(r'address', AddressViewSet, base_name="address")

#buycart--->url
router.register(r'shopcarts', ShoppingCartViewSet, base_name="shopcarts")

#order--->url
router.register(r'orders', OrderViewSet, base_name="orders")

# goods_list = GoodsListViewSet.as_view({
#     'get': 'list'
# })

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # url(r'^goods/$', goods_list, name='goods-list'),
    url(r'^', include(router.urls)),
    url(r'^index/', TemplateView.as_view(template_name='index.html'), name='index'),
    #drf Token check model
    url(r'^api-token-auth/', views.obtain_auth_token),
    #jwt-check-model
    url(r'^login/$', obtain_jwt_token),
    url(r'^docs/', include_docs_urls(title='my shop')),
    url(r'^alipay/return/', AliPayView.as_view(), name='alipay'),
    url('', include('social_django.urls', namespace='social'))
]
