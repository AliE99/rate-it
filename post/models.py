from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

    def average_rating(self):
        return self.ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0.0

    def rating_count(self):
        return self.ratings.count()


class Rating(models.Model):
    post = models.ForeignKey(Post, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.post.title} with {self.rating}"
