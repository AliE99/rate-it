from django.db import transaction
from rest_framework import serializers

from .models import Rating, Post


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['post', 'user', 'rating']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        post = validated_data['post']
        user = validated_data['user']
        new_rating = validated_data['rating']

        with transaction.atomic():
            rating, created = Rating.objects.get_or_create(
                post=post,
                user=user,
                defaults={'rating': new_rating}
            )

            if not created:
                old_rating = rating.rating
                rating.rating = new_rating
                rating.save()

                total_rating = post.average_rating * post.rating_count - old_rating + new_rating
            else:
                post.rating_count += 1
                total_rating = post.average_rating * (post.rating_count - 1) + new_rating

            post.average_rating = total_rating / post.rating_count
            post.save()

        return rating


class PostSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'average_rating', 'rating_count', 'user_rating']

    def get_user_rating(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            rating = Rating.objects.filter(post=obj, user=user).first()
            return rating.rating if rating else None
        return None
