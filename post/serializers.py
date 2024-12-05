from rest_framework import serializers

from .models import Rating, Post
from .tasks import update_post_average_rating


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

        rating, created = Rating.objects.get_or_create(
            post=post,
            user=user,
            defaults={'rating': new_rating}
        )
        update_post_average_rating.delay(post.id, rating.id, new_rating, created)

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
