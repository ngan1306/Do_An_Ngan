from django.contrib.auth import get_user_model
from novels.models import Category, Novel, Chapter
from django.core.files.base import ContentFile
import requests
from django.utils.text import slugify

def fetch_image(url):
    response = requests.get(url)
    return ContentFile(response.content)

def seed_data():
    # Tạo thể loại
    categories = [
        {'name': 'Đam Mỹ', 'slug': 'dam-my'},
        {'name': 'Ngôn Tình', 'slug': 'ngon-tinh'},
        {'name': 'Xuyên Không', 'slug': 'xuyen-khong'},
        {'name': 'Trọng Sinh', 'slug': 'trong-sinh'},
    ]
    
    for category_data in categories:
        Category.objects.get_or_create(
            name=category_data['name'],
            slug=category_data['slug']
        )
    
    # Tạo tác giả
    User = get_user_model()
    author, _ = User.objects.get_or_create(
        username='tacgia',
        email='tacgia@example.com',
        is_author=True
    )
    author.set_password('password123')
    author.save()
    
    # Tạo truyện
    novels = [
        {
            'title': 'Thiên Tài Đệ Nhất',
            'description': 'Một câu chuyện về tình yêu giữa hai thiên tài trong giới học thuật.',
            'categories': ['dam-my'],
            'chapters': [
                {'title': 'Chương 1: Cuộc gặp gỡ', 'content': 'Nội dung chương 1...'},
                {'title': 'Chương 2: Những ngày đầu', 'content': 'Nội dung chương 2...'},
            ]
        },
        {
            'title': 'Tình Yêu Vượt Thời Gian',
            'description': 'Một câu chuyện tình yêu xuyên không gian và thời gian.',
            'categories': ['ngon-tinh', 'xuyen-khong'],
            'chapters': [
                {'title': 'Chương 1: Lạc vào quá khứ', 'content': 'Nội dung chương 1...'},
                {'title': 'Chương 2: Gặp gỡ định mệnh', 'content': 'Nội dung chương 2...'},
            ]
        },
        {
            'title': 'Trọng Sinh Chi Vương Phi',
            'description': 'Một câu chuyện về một cô gái được trọng sinh và thay đổi số phận.',
            'categories': ['ngon-tinh', 'trong-sinh'],
            'chapters': [
                {'title': 'Chương 1: Trọng sinh', 'content': 'Nội dung chương 1...'},
                {'title': 'Chương 2: Gặp lại người xưa', 'content': 'Nội dung chương 2...'},
            ]
        }
    ]
    
    for novel_data in novels:
        novel = Novel.objects.create(
            title=novel_data['title'],
            description=novel_data['description'],
            author=author,
            slug=slugify(novel_data['title'])
        )
        
        # Thêm ảnh bìa
        novel.cover.save(
            f"{novel.slug}.jpg",
            fetch_image("https://picsum.photos/400/600"),
            save=True
        )
        
        # Thêm thể loại
        for category_slug in novel_data['categories']:
            category = Category.objects.get(slug=category_slug)
            novel.categories.add(category)
        
        # Thêm chương
        for i, chapter_data in enumerate(novel_data['chapters'], 1):
            Chapter.objects.create(
                novel=novel,
                title=chapter_data['title'],
                content=chapter_data['content'],
                chapter_number=i
            )
    
    print("Đã thêm dữ liệu mẫu thành công!")

if __name__ == '__main__':
    seed_data() 