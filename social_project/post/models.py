from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse as dj_reverse
from rest_framework.reverse import reverse as drf_reverse



class Post(models.Model):
    """ Model representing a post instance (for a simple Social Network).
    """
    title   = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(max_length=500, null=True, blank=True)

    posted  = models.DateTimeField(default=timezone.now)
    
    owner   = models.ForeignKey(
                                User,
                                related_name='posts',
                                blank=True,
                                on_delete=models.CASCADE
                                )
            
    liked = models.ManyToManyField(
                                User,
                                default=None,
                                blank=True,
                                related_name='liked',
                                )    
    
    
    class Meta:
        ordering = ['-posted']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return dj_reverse('dj-post-detail', kwargs={'pk': self.pk})

    def get_api_url(self, request=None):
        return drf_reverse("post-detail", kwargs={'pk': self.pk})

    def get_like_url(self):
        return dj_reverse("dj-post-like-toggle", kwargs={'pk': self.pk})
       
    def get_api_like_url(self):
        return drf_reverse("post-like-api-toggle", kwargs={'pk': self.pk})

    @property
    def liked_count(self):
        return self.liked.count
