from django.contrib.auth import tokens
from django.db.models import fields
from rest_framework import serializers
from . models import Profile
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes,smart_str,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed

# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
# from . utils import Util

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("attrs>>>>>>>",attrs)
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username
        data = super(CustomTokenObtainPairSerializer, self).validate(credentials)
        # Custom data you want to include
        data.update({'user': self.user.username})
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data


class RegistrationSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model=User
        fields=['username','email','password','confirm_password']
        extra_kwargs={'password':{'write_only':True,'required':'Please Enter Password'}}

    # def validate_email(self, email):
    #     existing=User.objects.filter(email=email)
    #     if existing:
    #         raise serializers.ValidationError("Someone with that email "
    #             "address has already registered. Was it you?")
    #     return email

    def validate(self, data):
        existing=User.objects.filter(email= data.get('email'))
        if existing:
            raise serializers.ValidationError("Someone with that email "
                "address has already registered. Was it you?")
        existing_username=User.objects.filter(username= data.get('username'))
        if existing_username:
            raise serializers.ValidationError("Someone with that Username has already registered. Was it you?")
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        print("validate data>>>>>>>>>",validated_data)
        confirm_password=validated_data.pop('confirm_password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
 
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        # if attrs['password'] != attrs['password2']:
        #     raise serializers.ValidationError({"password": "Password fields didn't match."})

        if not attrs.get('password') or not attrs.get('password2'):
            raise serializers.ValidationError("Please enter a password and confirm it.")
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError("Those passwords don't match.")

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=2)

    class Meta:
        fields=['email']

    # def validate(self, attrs):
    #     email=attrs['data'].get('email','')
    #     if User.objects.filter(email=email).exists():
    #         user=User.objects.filter(email=email)
    #         uidb64=urlsafe_base64_encode(user.id)
    #         token=PasswordResetTokenGenerator().make_token(user)
    #         current_site=get_current_site(request=attrs['data'].get('request')).domain
    #         relativeLink=reverse('password-reset',kwargs={'udid64':uidb64,'token':token})
    #         absurl='http://'+current_site+relativeLink
    #         email_body='Hello \n,Use the Link below to reset your password \n'
    #         data={'email_body':email_body,'to_email':user.email,'email_subject':'Reset Your Password'

    #         }
    #         Util.send_email(data)    
    #     return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    password2=serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password','password2', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            if not attrs.get('password') or not attrs.get('password2'):
                raise serializers.ValidationError("Please enter a password and confirm it.")
            if attrs.get('password') != attrs.get('password2'):
                raise serializers.ValidationError("Those passwords don't match.")
            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)