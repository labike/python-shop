# -*- coding: utf-8 -*-

__author__ = 'labike'


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from user_operation.models import UserFav
User = get_user_model()


@receiver(post_save, sender=User)
def create_userFav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=User)
def delete_userFav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()