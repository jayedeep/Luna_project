from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from . models import Post,Category,Likes
from django.contrib.auth.models import User
from users.serializers import ProfileSerializers


class LikeUSerSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','id']


class AutherSerializers(serializers.ModelSerializer):
    profile=ProfileSerializers()   
    class Meta:
        model=User
        fields=['username','id','profile','email']

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"
        
class LikesSerializers(serializers.ModelSerializer):
    # users=AutherSerializers()

    class Meta:
        model=Likes
        fields="__all__"
        ['date_liked','id','likes','post','unlike','user']
        

class PostSerializers(serializers.ModelSerializer):
    # category=CategorySerializers()
    auther=AutherSerializers()
    likes_set=LikesSerializers(many=True)
    # ordering = ('-date_posted',) #add this line

    class Meta:
        model=Post
        fields=['id','category','title','image','content','auther','date_posted','likes_set']
        
class PostSerializersCreate(serializers.ModelSerializer):
   
    class Meta:
        model=Post
        fields='__all__'
        