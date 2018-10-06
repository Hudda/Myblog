import datetime

from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    topic_text = models.CharField(max_length=200, null=False)
    image = models.ImageField(null=True, blank=True)
    content_text = models.TextField(null=False)
    vote = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    pub_date = models.DateTimeField(null=True)

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.topic_text



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    def was_published_recently(self):
        now = timezone.now()
        return self.pub_date <= now

    def __str__(self):
        return self.text