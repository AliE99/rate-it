# serializers.py

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

        # Check if the user has already rated this post
        existing_rating: Rating = Rating.objects.filter(post=post, user=user).first()

        if existing_rating:
            # User has already rated, update the rating
            old_rating = existing_rating.rating
            existing_rating.rating = new_rating
            existing_rating.save()

            # Update the average rating based on the change
            self.__update_average_on_rating_change(post, old_rating, new_rating)
            return existing_rating

        # User has not rated yet, create a new rating
        self.__update_average_and_rating_count(post, new_rating)
        return super().create(validated_data)

    def __update_average_on_rating_change(self, post, old_rating, new_rating):
        post.average_rating = ((post.average_rating * post.rating_count) - old_rating + new_rating) / post.rating_count
        post.save()

    def __update_average_and_rating_count(self, post, rating):
        post.rating_count += 1
        post.average_rating = (post.average_rating * post.rating_count + rating) / post.rating_count
        post.save()


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
