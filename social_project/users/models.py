from django.db import models
from django.contrib.auth.models import User



# https://docs.djangoproject.com/en/3.0/topics/auth/default/
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/

class Profile(models.Model):
    """ Model representing a Profile instanse.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default/default_picture.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'