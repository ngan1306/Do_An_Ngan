from django import forms
from .models import Novel, Chapter, Category, CommentForNovel, Rating

class NovelForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ['title', 'description', 'category', 'status', 'cover_image', 'author_name']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên tác giả'
            }),
        }

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'content', 'chapter_number']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 20}),
        }

class CommentForNovelForm(forms.ModelForm):
    class Meta:
        model = CommentForNovel
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Viết bình luận...'})
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.RadioSelect(choices=[(i, f'{i} sao') for i in range(1, 6)])
        }