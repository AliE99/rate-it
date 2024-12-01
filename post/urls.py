from django.urls import path

from .views import RatePostView, PostRatingView, PostViewSet

urlpatterns = [
    path('', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list-create'),
    path('<int:post_id>/rate/', RatePostView.as_view(), name='rate-post'),
    path('<int:post_id>/ratings/', PostRatingView.as_view(), name='post-ratings'),

]
