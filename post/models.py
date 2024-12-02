from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    average_rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Rating(models.Model):
    post = models.ForeignKey(Post, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} rated {self.post.title} with {self.rating}"
