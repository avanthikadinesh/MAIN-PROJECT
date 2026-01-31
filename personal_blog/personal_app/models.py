from django.db import models
from django.contrib.auth.models import User


class Post(models.Model): title = models.CharField(max_length=200) 
content = models.TextField() 
author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='personal_posts') 
created_at = models.DateTimeField(auto_now_add=True) 
updated_at = models.DateTimeField(auto_now=True) 


def __str__(self): 
    return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True)

    followers = models.ManyToManyField(
        User,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.user.username

    
    
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sent", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received", on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    



    
