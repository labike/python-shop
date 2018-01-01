from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from utils.permissions import IsOwnerReadOnly
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
# Create your views here.


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        get user collect list
    retrieve:
        the goods collect or not collect
    create:
        collect goods
    """

    permission_classes = (IsAuthenticated, IsOwnerReadOnly)
    serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer

        return UserFavSerializer


class LeavingMessageViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,
                            mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    lsit:
        get user leaving message
    create:
        add leaving message
    delete:
        delete leaving message
    """
    permission_classes = (IsAuthenticated, IsOwnerReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    """
    address manage
    list:
        get address
    create:
        add address
    update:
        update address
    delete:
        delete address
    """
    permission_classes = (IsAuthenticated, IsOwnerReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)



