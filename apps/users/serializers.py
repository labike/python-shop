# -*- coding: utf-8 -*-

__author__ = 'labike'

import re
from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from shops.settings import REGEX_MOBILE
from datetime import timedelta
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        check mobile
        :param data:
        :return:
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('user has save')

        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('mobile is error')

        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError('the time not more than 60s')

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    user detail seralizer
    """
    class Meta:
        model = User
        fields = ('name', 'gender', 'birthday', 'email', 'mobile')


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, label='code', max_length=4,
                                 error_messages = {
                                     'blank': 'please enter code',
                                     'required': 'please enter code',
                                     'max_length': 'the code style is error',
                                     'min_length': 'the code style is error'
                                 },
                                 min_length=4)
    username = serializers.CharField(label='username', required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='user has saved')])

    password = serializers.CharField(
        style={
            'input_type': 'password'
        },
        label='password',
        write_only=True,
    )

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validated_code(self, code):
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data['username']).order_by('-add_time')
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_records = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_records.add_time:
                raise serializers.ValidationError('code is out')
            if last_records.code != code:
                raise serializers.ValidationError('code is error')
        else:
            raise serializers.ValidationError('code is error')

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')