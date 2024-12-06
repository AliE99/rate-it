from celery import shared_task
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Post, Rating


@shared_task
def update_post_average_rating(post_id, rating_id, new_rating: int, created: bool) -> None:
    post = get_object_or_404(Post, id=post_id)
    rating = get_object_or_404(Rating, id=rating_id)

    with transaction.atomic():
        if not created:
            old_rating = rating.rating
            rating.rating = new_rating
            rating.save()

            total_rating = post.average_rating * post.rating_count - old_rating + new_rating
        else:
            post.rating_count += 1
            total_rating = post.average_rating * (post.rating_count - 1) + new_rating

        post.average_rating = total_rating / post.rating_count

        if post.rating_count == 1:
            post.ema_rating = new_rating
        else:
            post.ema_rating = Post.ALPHA * new_rating + (1 - Post.ALPHA) * post.ema_rating

        post.save()
