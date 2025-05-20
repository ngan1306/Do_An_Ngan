from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

@login_required
def create_novel(request):
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES)
        if form.is_valid():
            novel = form.save(commit=False)
            novel.author = request.user
            novel.save()
            form.save_m2m()
            return redirect('novels:novel_detail', slug=novel.slug)
    else:
        form = NovelForm()
    return render(request, 'novels/create_novel.html', {'form': form})

@login_required
def edit_novel(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    if request.user != novel.author and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES, instance=novel)
        if form.is_valid():
            form.save()
            return redirect('novels:novel_detail', slug=novel.slug)
    else:
        form = NovelForm(instance=novel)
    return render(request, 'novels/edit_novel.html', {'form': form, 'novel': novel})

@login_required
def delete_novel(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    if request.user != novel.author and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        novel.delete()
        return redirect('novels:novel_list')
    return render(request, 'novels/delete_novel.html', {'novel': novel})

@login_required
def create_chapter(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    if request.user != novel.author and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.novel = novel
            chapter.save()
            return redirect('novels:chapter_detail', slug=novel.slug, chapter_number=chapter.chapter_number)
    else:
        form = ChapterForm()
    return render(request, 'novels/create_chapter.html', {'form': form, 'novel': novel})

@login_required
def edit_chapter(request, slug, chapter_number):
    novel = get_object_or_404(Novel, slug=slug)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)
    if request.user != novel.author and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            return redirect('novels:chapter_detail', slug=novel.slug, chapter_number=chapter.chapter_number)
    else:
        form = ChapterForm(instance=chapter)
    return render(request, 'novels/edit_chapter.html', {'form': form, 'novel': novel, 'chapter': chapter})

@login_required
def delete_chapter(request, slug, chapter_number):
    novel = get_object_or_404(Novel, slug=slug)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)
    if request.user != novel.author and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        chapter.delete()
        return redirect('novels:novel_detail', slug=novel.slug)
    return render(request, 'novels/delete_chapter.html', {'novel': novel, 'chapter': chapter})

@login_required
def add_comment(request, slug, chapter_number):
    chapter = get_object_or_404(Chapter, novel__slug=slug, chapter_number=chapter_number)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.chapter = chapter
            comment.user = request.user
            comment.save()
            messages.success(request, 'Bình luận đã được đăng thành công!')
    return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_staff:
        comment.delete()
        messages.success(request, 'Bình luận đã được xóa!')
    return redirect('novels:chapter_detail', slug=comment.chapter.novel.slug, chapter_number=comment.chapter.chapter_number)

@login_required
def add_novel_comment(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    if request.method == 'POST':
        form = CommentForNovelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.novel = novel
            comment.user = request.user
            comment.save()
            messages.success(request, 'Bình luận đã được đăng thành công!')
    return redirect('novels:novel_detail', slug=slug)

@login_required
def delete_novel_comment(request, comment_id):
    comment = get_object_or_404(CommentForNovel, id=comment_id)
    if request.user == comment.user or request.user.is_staff:
        comment.delete()
        messages.success(request, 'Bình luận đã được xóa!')
    return redirect('novels:novel_detail', slug=comment.novel.slug) 