from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Novel, Chapter, Category, ReadingHistory, CommentForNovel, Rating, NovelFollow, Comment
from .forms import NovelForm, ChapterForm, CommentForNovelForm, RatingForm
from django.utils import timezone
from django.http import JsonResponse

def novel_list(request, category_slug=None):
    query = request.GET.get('q')
    
    novels = Novel.objects.all()
    
    if query:
        novels = novels.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            novels = novels.filter(category=category)
        except Category.DoesNotExist:
            messages.warning(request, f"Thể loại '{category_slug}' không tồn tại.")
    
    categories = Category.objects.all()
    return render(request, 'novels/list.html', {
        'novels': novels,
        'categories': categories,
        'query': query,
        'current_category': category_slug
    })

def novel_detail(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    chapters = novel.chapters.all()
    avg_rating = novel.ratings.aggregate(Avg('score'))['score__avg']
    is_following = False
    if request.user.is_authenticated:
        is_following = novel.followers.filter(user=request.user).exists()
        novel.views += 1
        novel.save()
    return render(request, 'novels/detail.html', {
        'novel': novel,
        'chapters': chapters,
        'avg_rating': avg_rating,
        'is_following': is_following,
    })

@login_required
def create_novel(request):
    if not request.user.is_author:
        messages.error(request, 'Bạn không có quyền tạo truyện.')
        return redirect('novels:novel_list')
    
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES)
        if form.is_valid():
            novel = form.save(commit=False)
            novel.author = request.user
            novel.save()
            messages.success(request, 'Truyện đã được tạo thành công!')
            return redirect('novels:novel_detail', slug=novel.slug)
    else:
        form = NovelForm()
    
    return render(request, 'novels/novel_form.html', {
        'form': form,
        'title': 'Tạo truyện mới'
    })

@login_required
def edit_novel(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    
    if novel.author != request.user and not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền chỉnh sửa truyện này.')
        return redirect('novels:novel_detail', slug=novel.slug)
    
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES, instance=novel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Truyện đã được cập nhật thành công.')
            return redirect('novels:novel_detail', slug=novel.slug)
    else:
        form = NovelForm(instance=novel)
    return render(request, 'novels/novel_form.html', {
        'form': form,
        'title': 'Chỉnh sửa truyện',
        'novel': novel
    })

@login_required
def create_chapter(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    
    # Kiểm tra quyền tác giả
    if request.user != novel.author and not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền thêm chương cho truyện này.')
        return redirect('novels:novel_detail', slug=novel.slug)
    
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.novel = novel
            
            # Kiểm tra xem số chương đã tồn tại chưa
            if Chapter.objects.filter(novel=novel, chapter_number=chapter.chapter_number).exists():
                messages.error(request, f'Chương {chapter.chapter_number} đã tồn tại.')
                return redirect('novels:novel_detail', slug=novel.slug)
            
            chapter.save()
            messages.success(request, f'Đã thêm chương {chapter.chapter_number}: {chapter.title}')
            return redirect('novels:chapter_detail', slug=novel.slug, chapter_number=chapter.chapter_number)
    else:
        form = ChapterForm()
    
    return render(request, 'novels/create_chapter.html', {
        'form': form,
        'novel': novel
    })

def chapter_detail(request, slug, chapter_number):
    novel = get_object_or_404(Novel, slug=slug)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)
    
    if request.user.is_authenticated:
        chapter.views += 1
        chapter.save()
        
        ReadingHistory.objects.update_or_create(
            user=request.user,
            chapter=chapter,
            defaults={'last_read': timezone.now()}
        )
    
    return render(request, 'novels/chapter_detail.html', {
        'novel': novel,
        'chapter': chapter
    })

@login_required
def edit_chapter(request, slug, chapter_number):
    novel = get_object_or_404(Novel, slug=slug)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)
    
    # Check if user has permission to edit
    if request.user != novel.author and not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền chỉnh sửa chương này.')
        return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)
    
    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chương đã được cập nhật thành công.')
            return redirect('novels:chapter_detail', slug=novel.slug, chapter_number=chapter.chapter_number)
    else:
        form = ChapterForm(instance=chapter)
    return render(request, 'novels/edit_chapter.html', {'form': form, 'novel': novel, 'chapter': chapter})

@login_required
def favorite_novels(request):
    novels = request.user.favorite_novels.all()
    return render(request, 'novels/favorite_list.html', {
        'novels': novels,
        'title': 'Truyện yêu thích'
    })

@login_required
def toggle_favorite(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    if novel in request.user.favorite_novels.all():
        request.user.favorite_novels.remove(novel)
        messages.success(request, 'Đã xóa khỏi danh sách yêu thích.')
    else:
        request.user.favorite_novels.add(novel)
        messages.success(request, 'Đã thêm vào danh sách yêu thích.')
    return redirect('novels:novel_detail', slug=slug)

@login_required
def create_novel(request):
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES)
        if form.is_valid():
            novel = form.save(commit=False)
            novel.author = request.user
            novel.save()
            messages.success(request, 'Truyện đã được tạo thành công!')
            return redirect('novels:novel_detail', slug=novel.slug)
    else:
        form = NovelForm()
    
    return render(request, 'novels/novel_form.html', {
        'form': form,
        'title': 'Tạo truyện mới'
    })

@login_required
def novel_edit(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    
    if novel.author != request.user and not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền chỉnh sửa truyện này.')
        return redirect('novels:novel_detail', slug=novel.slug)
    
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES, instance=novel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Truyện đã được cập nhật thành công!')
            return redirect('novels:novel_detail', slug=novel.slug)
    else:
        form = NovelForm(instance=novel)
    
    return render(request, 'novels/novel_form.html', {
        'form': form,
        'title': 'Chỉnh sửa truyện',
        'novel': novel
    })

@login_required
def delete_novel(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    if request.user == novel.author or request.user.is_staff:
        novel.delete()
        messages.success(request, "Truyện đã được xóa thành công.")
        return redirect('novels:novel_list')
    else:
        messages.error(request, "Bạn không có quyền xóa truyện này.")
        return redirect('novels:novel_detail', slug=slug)

@login_required
def delete_chapter(request, slug, chapter_number):
    novel = get_object_or_404(Novel, slug=slug)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)
    if request.user == novel.author or request.user.is_staff:
        chapter.delete()
        messages.success(request, "Chương đã được xóa thành công.")
        return redirect('novels:novel_detail', slug=slug)
    else:
        messages.error(request, "Bạn không có quyền xóa chương này.")
        return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)

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

@login_required
def rate_novel(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    try:
        rating = Rating.objects.get(novel=novel, user=request.user)
    except Rating.DoesNotExist:
        rating = None

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            new_rating = form.save(commit=False)
            new_rating.novel = novel
            new_rating.user = request.user
            new_rating.save()
            messages.success(request, 'Bạn đã đánh giá truyện này!')
            return redirect('novels:novel_detail', slug=slug)
    else:
        form = RatingForm(instance=rating)

    return render(request, 'novels/rate_novel.html', {'form': form, 'novel': novel})

@login_required
def toggle_follow(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    follow, created = NovelFollow.objects.get_or_create(user=request.user, novel=novel)
    if not created:
        follow.delete()
        messages.success(request, "Đã bỏ theo dõi truyện.")
    else:
        messages.success(request, "Đã theo dõi truyện.")
    return redirect('novels:novel_detail', slug=slug)

@login_required
def followed_novels(request):
    follows = NovelFollow.objects.filter(user=request.user).select_related('novel')
    novels = [f.novel for f in follows]
    return render(request, 'novels/followed_list.html', {'novels': novels, 'title': 'Truyện đang theo dõi'})

@login_required
def add_chapter_comment(request, slug, chapter_number):
    novel = get_object_or_404(Novel, slug=slug)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                chapter=chapter,
                user=request.user,
                content=content
            )
            messages.success(request, 'Bình luận đã được thêm thành công!')
        else:
            messages.error(request, 'Nội dung bình luận không được để trống!')
    
    return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)

@login_required
def delete_chapter_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Kiểm tra xem người dùng có quyền xóa bình luận không
    if comment.user == request.user or request.user.is_staff:
        chapter = comment.chapter
        comment.delete()
        messages.success(request, 'Bình luận đã được xóa thành công!')
        return redirect('novels:chapter_detail', slug=chapter.novel.slug, chapter_number=chapter.chapter_number)
    else:
        messages.error(request, 'Bạn không có quyền xóa bình luận này!')
        return redirect('novels:chapter_detail', slug=comment.chapter.novel.slug, chapter_number=comment.chapter.chapter_number)

@login_required
def split_chapter(request, slug, chapter_number):
    novel = get_object_or_404(Novel, slug=slug)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)
    
    # Kiểm tra quyền tác giả
    if request.user != novel.author and not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền tách chương này.')
        return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)
    
    if request.method == 'POST':
        split_point = request.POST.get('split_point')
        if not split_point:
            messages.error(request, 'Vui lòng chọn điểm tách chương.')
            return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)
            
        try:
            split_point = int(split_point)
            content = chapter.content.split('\n')
            if split_point <= 0 or split_point >= len(content):
                messages.error(request, 'Điểm tách không hợp lệ.')
                return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)
                
            # Tạo chương mới
            new_chapter = Chapter.objects.create(
                novel=novel,
                title=f"{chapter.title} (Phần 2)",
                content='\n'.join(content[split_point:]),
                chapter_number=chapter.chapter_number + 1
            )
            
            # Cập nhật chương cũ
            chapter.content = '\n'.join(content[:split_point])
            chapter.title = f"{chapter.title} (Phần 1)"
            chapter.save()
            
            # Cập nhật số chương của các chương sau
            chapters_to_update = Chapter.objects.filter(
                novel=novel,
                chapter_number__gt=new_chapter.chapter_number
            ).order_by('chapter_number')
            
            for ch in chapters_to_update:
                ch.chapter_number += 1
                ch.save()
            
            messages.success(request, 'Đã tách chương thành công!')
            return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter.chapter_number)
            
        except ValueError:
            messages.error(request, 'Điểm tách không hợp lệ.')
            return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)
    
    return render(request, 'novels/split_chapter.html', {
        'novel': novel,
        'chapter': chapter
    })

@login_required
def add_author_note(request, slug, chapter_number):
    novel = get_object_or_404(Novel, slug=slug)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)
    
    if request.user != novel.author and not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền thêm ghi chú tác giả.')
        return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)
    
    if request.method == 'POST':
        author_note = request.POST.get('author_note')
        chapter.author_note = author_note
        chapter.save()
        messages.success(request, 'Đã cập nhật ghi chú tác giả.')
    
    return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)

@login_required
def edit_author_note(request, slug, chapter_number):
    novel = get_object_or_404(Novel, slug=slug)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)
    
    if request.user != novel.author and not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền chỉnh sửa thông tin tác giả.')
        return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)
    
    if request.method == 'POST':
        author_text = request.POST.get('author_text')
        chapter.author_text = author_text
        chapter.save()
        messages.success(request, 'Đã cập nhật thông tin tác giả.')
    
    return redirect('novels:chapter_detail', slug=slug, chapter_number=chapter_number)