from django.db import models
from django.conf import settings
from blog.models import Post


class Visitor(models.Model):
    ip = models.CharField(max_length=45)
    path = models.CharField(max_length=255)
    user_agent = models.TextField(blank=True)
    referrer = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip} @ {self.timestamp:%Y-%m-%d %H:%M} -> {self.path}"


class PortalPost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='portal')
    visible = models.BooleanField(default=True, help_text='Whether this post is visible on the public blog')

    def __str__(self):
        return f"Portal settings for {self.post.title}"
