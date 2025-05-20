from django.db import models
from django.contrib.auth import get_user_model
from novels.models import Novel, Chapter

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_chapter', 'Chương mới'),
        ('novel_update', 'Cập nhật truyện'),
        ('system', 'Thông báo hệ thống'),
        ('comment', 'Bình luận'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}" 