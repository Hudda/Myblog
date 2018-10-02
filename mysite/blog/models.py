import datetime

from django.db import models
from django.utils import timezone

class Post(models.Model):
    topic_text = models.CharField(max_length=200, null=False)
    content_text = models.TextField(null=False)
    vote = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.topic_text



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text