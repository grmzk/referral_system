from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User
from users.validators import (auth_code_regex_validator,
                              username_regex_validator)


class ReferrerField(serializers.RelatedField):
    def to_representation(self, referrer):
        return referrer.invite_code

    def to_internal_value(self, invite_code):
        user = self.context['request'].user
        if user.invite_code == invite_code:
            raise serializers.ValidationError('It is forbidden to specify '
                                              'your own invite_code!')
        if user.referrer:
            raise serializers.ValidationError('Referrer was '
                                              'already specified!')
        referrer = User.objects.filter(invite_code=invite_code).first()
        if not referrer:
            raise serializers.ValidationError('Invalid invite_code!')
        return referrer


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=12,
                                     validators=[username_regex_validator])
    referrer_invite_code = ReferrerField(source='referrer',
                                         queryset=User.objects.all())
    referrals = serializers.SerializerMethodField()

    class Meta:
        fields = ['username', 'invite_code', 'referrer_invite_code',
                  'referrals']
        read_only_fields = ['username', 'invite_code', 'referrals']
        model = User

    @staticmethod
    def get_referrals(user):
        return User.objects.filter(referrer=user).values_list('username',
                                                              flat=True)


class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,
                                     max_length=12,
                                     validators=[username_regex_validator])

    class Meta:
        fields = ['username']
        model = User


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150,
                                     validators=[username_regex_validator])
    auth_code = serializers.CharField(required=True, max_length=4,
                                      validators=[auth_code_regex_validator])

    def validate(self, attrs):
        username = attrs['username']
        auth_code = attrs['auth_code']
        user = get_object_or_404(User, username=username)
        if not user.auth_code:
            raise serializers.ValidationError('Get the auth_code by SMS!')
        if user.auth_code != auth_code:
            raise serializers.ValidationError('Invalid auth_code!')
        user.auth_code = None
        user.save()
        return attrs
