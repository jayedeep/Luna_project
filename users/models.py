from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.shortcuts import reverse
from django.core.files.storage import default_storage as storage

# Create your models here.

# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(_('email address'), unique=True)
#     user_name = models.CharField(max_length=150, unique=True)
#     first_name = models.CharField(max_length=150, blank=True)
#     start_date = models.DateTimeField(default=timezone.now)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')
    description=models.CharField(max_length=300)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('profile-detail',kwargs={'pk':self.pk})

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)
        
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img=Image.open(self.image)
        
        if img.height >300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image)


    # def save(self,):
    #     super().save(*args,**kwargs)
    #     # img=Image.open(self.image.path)
    #     image = Image.open(self.image.path)
    #     cropped_image = image.crop((x, y, w + x, h + y))
    #     resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)

    #     fh = storage.open(user.primaryphoto.name, "w")
    #     picture_format = 'png'
    #     resized_image.save(fh, picture_format)
    #     fh.close()        
    #     resized_image.save(user.primaryphoto.path)
    #     return user