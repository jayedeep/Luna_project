from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Post,Likes
from .serializers import PostSerializers,LikeUSerSerializers,PostSerializersCreate,CategorySerializers,LikesSerializers
from rest_framework.generics import (ListAPIView,CreateAPIView,
                                    RetrieveUpdateDestroyAPIView)

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import filters
from django.contrib.auth.models import User
import django_filters
from distutils.util import strtobool
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class PostListView(ListAPIView):
    queryset=Post.objects.all()
    serializer_class= PostSerializers
    authentication_classes=[JWTAuthentication]
    permission_classes=[AllowAny]

class PostCreate(CreateAPIView):
    queryset=Post.objects.all()
    serializer_class= PostSerializersCreate
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class PostRetriveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class= PostSerializers
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class PostListSearch(ListAPIView):
    queryset=Post.objects.all()
    permission_classes=[AllowAny]
    serializer_class= PostSerializers
    filter_backends=[filters.SearchFilter]
    search_fields=['^title','^content','^auther__username']


BOOLEAN_CHOICES = (('false', 'False'), ('true', 'True'),)

class CustomFilterList(django_filters.Filter):
    def filter(self, qs, value):
        if value not in (None, ''):
            values = [v for v in value.split(',')]
            return qs.filter(**{'%s__%s' % (self.field_name, self.lookup_expr): values})
        return qs


class PostFilter(django_filters.FilterSet):
    #     # category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), widget = CheckboxSelectMultiple)

    date_posted = django_filters.DateFromToRangeFilter()
    category = CustomFilterList(field_name="category", lookup_expr="in")

    class Meta:
        model = Post     
        fields = ['category']

class PostListFilter(ListAPIView):
    queryset=Post.objects.all()
    permission_classes=[AllowAny]
    serializer_class= PostSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    # filter_fields = ('category', 'date_posted')


#-------------- 
class CategoryListView(ListAPIView):
    queryset=Category.objects.all()
    serializer_class= CategorySerializers
    permission_classes=[AllowAny]

class CategoryCreate(CreateAPIView):
    queryset=Category.objects.all()
    serializer_class= CategorySerializers

class CategoryRetriveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset=Category.objects.all()
    serializer_class= CategorySerializers


#-----------------------

class LikesListView(ListAPIView):
    queryset=Likes.objects.all()
    serializer_class= LikesSerializers
  
class LikesCreate(CreateAPIView):
    queryset=Likes.objects.all()
    serializer_class= LikesSerializers
    permission_classes=[IsAuthenticated]
    # authentication_classes=[JWTAuthentication]
    def post(self, request, *args, **kwargs):
        # request.data['auther']=request.user
        print(">>>>>>>>>>>>>put custom",request,request.data)
        return self.create(request, *args, **kwargs)

class LikesRetriveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset=Likes.objects.all()
    serializer_class= LikesSerializers
    permission_classes=[IsAuthenticated]

class LikeListByUserIds(APIView):
    def get(self,request,format='json'):
        user_ids=self.request.query_params.get('userids')
        user_ids=user_ids.split(",")
        users=User.objects.filter(id__in=user_ids)
        serializer=LikeUSerSerializers(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

def about(request):
    return render(request,'blog/about.html',{'title':"about"})
