from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication

from rest_framework import viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Goods, GoodsCategory, HotSearchWords, Banner
from .filters import GoodsFilter
from .serializers import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializer
from .serializers import IndexCategorySerializer

# Create your views here.


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List all goods, include pagination, search, filter, order_by
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     price_min = self.request.query_params.get('price_min', 0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        category list
    retrieve:
        category detail
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    hotwords list
    """
    queryset = HotSearchWords.objects.all().order_by('-index')
    serializer_class= HotWordsSerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    slider image list
    """
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    index goods category data
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '酒水饮料'])
    serializer_class = IndexCategorySerializer



