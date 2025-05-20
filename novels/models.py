from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Novel(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Đang tiến hành'),
        ('completed', 'Đã hoàn thành'),
        ('hiatus', 'Tạm ngưng'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='novels')
    author_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Author')
    description = models.TextField()
    cover_image = models.ImageField(upload_to='novel_covers/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='novels')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    favorites = models.ManyToManyField(User, related_name='favorite_novels', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    content = models.TextField()
    chapter_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    author_note = models.TextField(blank=True, null=True)
    author_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['chapter_number']
        unique_together = ['novel', 'chapter_number']

    def __str__(self):
        return f"{self.novel.title} - Chương {self.chapter_number}: {self.title}"

class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_history')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    last_read = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'chapter']

    def __str__(self):
        return f"{self.user.username} - {self.chapter}"

class CommentForNovel(models.Model):
    novel = models.ForeignKey('Novel', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.novel}'

class Rating(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 sao
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('novel', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.novel.title}: {self.score} sao"

class NovelFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='novel_follows')
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'novel')

    def __str__(self):
        return f"{self.user.username} theo dõi {self.novel.title}"

class Comment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on chapter {self.chapter.chapter_number}'