from rest_framework import serializers
from .models import Novel, Chapter, NovelFollow, Rating, CommentForNovel, Comment

class NovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = ['id', 'title', 'author', 'description', 'cover_image', 'status', 'category', 'slug', 'views']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'novel', 'title', 'content', 'chapter_number', 'created_at', 'updated_at', 'views']

class NovelFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = NovelFollow
        fields = ['id', 'user', 'novel', 'followed_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'novel', 'score', 'created_at']

class CommentForNovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentForNovel
        fields = ['id', 'novel', 'user', 'content', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'chapter', 'user', 'content', 'created_at', 'updated_at'] 