from django.urls import path

from .views import RatePostView, PostRatingView

urlpatterns = [
    path('', PostRatingView.as_view(), name='posts'),
    path('<int:post_id>/rate/', RatePostView.as_view(), name='rate-post'),
    path('<int:post_id>/ratings/', PostRatingView.as_view(), name='post-ratings'),

]
