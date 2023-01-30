from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    forget_password_token = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    # profile_image = models.ImageField(upload_to = 'profile')

    def __str__(self):
        return self.user.username