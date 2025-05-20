from django.urls import path
from . import api_views

urlpatterns = [
    # Novel CRUD
    path('novels/', api_views.NovelListCreateAPI.as_view(), name='api_novel_list_create'),
    path('novels/<slug:slug>/', api_views.NovelDetailAPI.as_view(), name='api_novel_detail'),
    # Chapter CRUD
    path('novels/<slug:slug>/chapters/', api_views.ChapterListCreateAPI.as_view(), name='api_chapter_list_create'),
    path('chapters/<int:id>/', api_views.ChapterDetailAPI.as_view(), name='api_chapter_detail'),
    # Follow
    path('follows/', api_views.NovelFollowListCreateAPI.as_view(), name='api_follow_list_create'),
    path('follows/<int:id>/', api_views.NovelFollowDeleteAPI.as_view(), name='api_follow_delete'),
    # Rating
    path('ratings/', api_views.RatingListCreateAPI.as_view(), name='api_rating_list_create'),
    path('ratings/<int:id>/', api_views.RatingDetailAPI.as_view(), name='api_rating_detail'),
    # Comment for Novel
    path('novels/<slug:slug>/comments/', api_views.CommentForNovelListCreateAPI.as_view(), name='api_novel_comment_list_create'),
    path('novel_comments/<int:id>/', api_views.CommentForNovelDeleteAPI.as_view(), name='api_novel_comment_delete'),
    # Comment for Chapter
    path('chapters/<int:chapter_id>/comments/', api_views.CommentListCreateAPI.as_view(), name='api_chapter_comment_list_create'),
    path('chapter_comments/<int:id>/', api_views.CommentDeleteAPI.as_view(), name='api_chapter_comment_delete'),
] 