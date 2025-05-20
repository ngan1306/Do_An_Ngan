class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Viết bình luận...'})
        } 

class CommentForNovelForm(forms.ModelForm):
    class Meta:
        model = CommentForNovel
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Viết bình luận...'})
        } 