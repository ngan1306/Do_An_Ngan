from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Novel, Chapter, NovelFollow, Rating, CommentForNovel, Comment
from .serializers import NovelSerializer, ChapterSerializer, NovelFollowSerializer, RatingSerializer, CommentForNovelSerializer, CommentSerializer

# --- Novel CRUD ---
class NovelListCreateAPI(generics.ListCreateAPIView):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class NovelDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --- Chapter CRUD ---
class ChapterListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        novel_slug = self.kwargs['slug']
        return Chapter.objects.filter(novel__slug=novel_slug)
    def perform_create(self, serializer):
        novel = Novel.objects.get(slug=self.kwargs['slug'])
        serializer.save(novel=novel)

class ChapterDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --- Follow API ---
class NovelFollowListCreateAPI(generics.ListCreateAPIView):
    serializer_class = NovelFollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return NovelFollow.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NovelFollowDeleteAPI(generics.DestroyAPIView):
    queryset = NovelFollow.objects.all()
    serializer_class = NovelFollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        return NovelFollow.objects.filter(user=self.request.user)

# --- Rating API ---
class RatingListCreateAPI(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RatingDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

# --- Comment for Novel API ---
class CommentForNovelListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CommentForNovelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        novel_slug = self.kwargs['slug']
        return CommentForNovel.objects.filter(novel__slug=novel_slug)
    def perform_create(self, serializer):
        novel = Novel.objects.get(slug=self.kwargs['slug'])
        serializer.save(novel=novel, user=self.request.user)

class CommentForNovelDeleteAPI(generics.DestroyAPIView):
    queryset = CommentForNovel.objects.all()
    serializer_class = CommentForNovelSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        return CommentForNovel.objects.filter(user=self.request.user)

# --- Comment for Chapter API ---
class CommentListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        chapter_id = self.kwargs['chapter_id']
        return Comment.objects.filter(chapter_id=chapter_id)
    def perform_create(self, serializer):
        chapter = Chapter.objects.get(id=self.kwargs['chapter_id'])
        serializer.save(chapter=chapter, user=self.request.user)

class CommentDeleteAPI(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user) 