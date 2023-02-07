
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListPosts.as_view(), name="index"),
    path("post", views.ListPosts.as_view(), name="post-list"),
    path("post/following", views.ListFollowingPosts.as_view(), name="post-following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/add", views.CreatePost.as_view(), name="post-create"),
    path("post/update/<int:pk>", views.UpdatePost.as_view(), name="post-update"),
    path("post/delete/<int:pk>", views.DeletePost.as_view(), name="post-delete"),
    path("api/post/add", views.AddPostAPI.as_view(), name="api-post-create" ),
    path("api/post/update/<int:pk>", views.UpdatePostAPI.as_view(), name="api-post-update" ),
    path("api/post/delete", views.DeletePostAPI.as_view(), name="api-post-update" ),
    path("api/post/all", views.ListPostsAPI.as_view(), name="api-post-all" ),
    path("api/post/following", views.ListFollowingPostsAPI.as_view(), name="api-post-following" ),
    path("api/post/profile/<int:pk>", views.ListFollowingProfileAPI.as_view(), name="api-post-following" ),

]
