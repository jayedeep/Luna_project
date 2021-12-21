from django.db import models
from django.db.models.base import Model
from django.utils import timezone
# from datetime import date
from django.utils.timezone import localdate
from django.contrib.auth.models import User
from django.shortcuts import reverse
# Create your models here.
from PIL import Image


class Category(models.Model):
    category=models.CharField(max_length=50)
    def __str__(self):
        return self.category

class Post(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    content=models.TextField()
    image=models.ImageField(upload_to='post_image',blank=True,null=True)
    date_posted=models.DateField(default=localdate)
    auther=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        ordering = ['-date_posted']

    
    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        # print(self.image,">>>>>>>>>>>image")
        if self.image:
            img=Image.open(self.image.path)

            if img.height >300 or img.width>300:
                output_size=(300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Likes(models.Model):
    likes=models.BooleanField(default=False)
    unlike=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    date_liked=models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return "liked"+str(self.likes)+str(self.user.username)