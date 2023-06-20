
from django.urls import path
from postsharing.views import (ExploreView, UserPage, PostListView, PostCreateView,
                         PostDetailView, PostUpdateView, 
                         PostDeleteView, add_comment,
                         add_like, toggle_follow_unfollow)

urlpatterns = [
    
    path('', ExploreView.as_view(), name='explore'),
 
    path('profile/<pk>', UserPage.as_view(), name='user_page'),

    path('posts/', PostListView.as_view(), name='posts'),
    path('make_post/', PostCreateView.as_view(), name='make_post'),
    path('post/<pk>/', PostDetailView.as_view(), name='post'),
    path('edit_post/<pk>/', PostUpdateView.as_view(), name='edit_post'),
    path('delete_post/<pk>', PostDeleteView.as_view(), name='delete_post'),

    path('add_comment/', add_comment, name='add_comment'), # type: ignore
    path('add_like/', add_like, name='add_like'), # type: ignore
    path('toggle_connection/', toggle_follow_unfollow, name='toggle_connection'), # type: ignore

]
