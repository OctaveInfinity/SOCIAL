from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User



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
            
    class Meta:
        ordering = ['-posted']

    def __str__(self):
        return self.title
