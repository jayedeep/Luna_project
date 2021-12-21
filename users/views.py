from django.shortcuts import render
from . serializers import RegistrationSerializers,RequestPasswordResetEmailSerializer,SetNewPasswordSerializer
from rest_framework import status
from django.core import serializers
from django.http import JsonResponse, request

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView,GenericAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from blog.models import Post
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
import json
from .models import Profile
from .serializers import ProfileSerializers,ChangePasswordSerializer
from blog.serializers import PostSerializers,AutherSerializers

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes,smart_str,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from . utils import Util


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    # def get_queryset(self):
    #     print(">>>>>>>>change password",self.request.user)
    #     return User.objects.filter(pk=self.request.user.pk)

    def put(self, request, *args, **kwargs):
        print(">>>>>><<<<changes request>//////",request.data)
        return self.update(request, *args, **kwargs)


class BlacklistTokenView(APIView):
    def post(self,request,format='json'):
        permission_classes = [AllowAny]
        try:
            refresh_token=request.data['refresh_token']
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':"Successfully Logged Out"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = RegistrationSerializers(data=request.data)
        if serializer.is_valid():
            user=User.objects.filter(username=request.data.get('username'))
            if not user:
                user = serializer.save()
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(serializer.errors,"456>>>>>>>>>>>>>>>>")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllUsers(APIView):
    def get(self,request,format='json'):

        usernames = [user.username for user in User.objects.all() if user.username != '' or False]
        emails=[user.email for user in User.objects.all() if user.email != '' or False]
        return Response({"usernames":usernames,"emails":emails})

class CurrentUserWithPost(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,format='json'):
        user=AutherSerializers(request.user)
        profile=ProfileSerializers(Profile.objects.get(user=request.user), context={"request": request})
        posts= PostSerializers(Post.objects.filter(auther=request.user),context={"request": request},many=True)
       
        return Response({"user":user.data,"posts":posts.data,'profile':profile.data})
    
    def patch(self,request,format='json'):
        # id=request.user.id
        print("request data put>>>>>>>>>",self.request.body,request.data)

        stu=Profile.objects.get(user=request.user)
        serializer=ProfileSerializers(stu,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProfileShower(APIView):
    def get(self,request,format='json'):
        user_id=int(self.request.query_params.get('userid'))
        user_obj=User.objects.get(id=user_id)

        # user= serializers.serialize('python',[user_obj])
        user= AutherSerializers(user_obj)

        
        profile=ProfileSerializers(Profile.objects.get(user=user_obj), context={"request": request})
        posts= PostSerializers(Post.objects.filter(auther=user_obj),context={"request": request},many=True)
        return Response({"user":user.data,"posts":posts.data,'profile':profile.data})

class RequestPasswordResetEmail(GenericAPIView):
    serializer_class=RequestPasswordResetEmailSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)

        email=request.data['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            current_site=get_current_site(request=request).domain
            relativeLink=reverse('password-reset',kwargs={'uid64':uidb64,'token':token})
            # relativeLink='password-reset'+'/'+uidb64+'/'
            # absurl='http://'+current_site+relativeLink
            print(relativeLink,">>>>>>>>>>>>>")
            relativeLink=relativeLink[4:]
            absurl='http://localhost:8000'+relativeLink

           
            email_body = 'Hi '+user.username + \
            ' Use the link below to Change The Password \n' + absurl
            data={'email_body':email_body,'to_email':user.email,'email_subject':'Reset Your Password'

            }
            Util.send_email(data)    

        serializer.is_valid(raise_exception=True)
        return Response({'success':"We have sent you a link to reset your password"},status=status.HTTP_200_OK)

class PasswordTokenCheckApi(GenericAPIView):
    # serializer_class = SetNewPasswordSerializer

    def get(self, request, uid64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is invalid,please request a new one'},status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'success':True,'message':'Credentials Valid','uid64':uid64,'token':token},status=status.HTTP_200_OK)
                # if len(redirect_url) > 3:
            #         return CustomRedirect(redirect_url+'?token_valid=False')
            #     else:
            #         return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            # if redirect_url and len(redirect_url) > 3:
            #     return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            # else:
            #     return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return Response({'error':'Token is invalid,please request a new one'},status=status.HTTP_400_BAD_REQUEST)
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)