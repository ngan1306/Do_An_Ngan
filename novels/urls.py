from django.urls import path
from . import views

app_name = 'novels'

urlpatterns = [
    path('', views.novel_list, name='novel_list'),
    path('category/<slug:category_slug>/', views.novel_list, name='novel_list_by_category'),
    path('create/', views.create_novel, name='create_novel'),
    path('favorites/', views.favorite_novels, name='favorite_novels'),
    path('<slug:slug>/', views.novel_detail, name='novel_detail'),
    path('<slug:slug>/edit/', views.edit_novel, name='edit_novel'),
    path('<slug:slug>/chapters/create/', views.create_chapter, name='create_chapter'),
    path('<slug:slug>/chapters/<int:chapter_number>/', views.chapter_detail, name='chapter_detail'),
    path('<slug:slug>/chapters/<int:chapter_number>/edit/', views.edit_chapter, name='edit_chapter'),
    path('<slug:slug>/chapters/<int:chapter_number>/delete/', views.delete_chapter, name='delete_chapter'),
    path('<slug:slug>/chapters/<int:chapter_number>/split/', views.split_chapter, name='split_chapter'),
    path('<slug:slug>/chapters/<int:chapter_number>/comment/', views.add_chapter_comment, name='add_chapter_comment'),
    path('<slug:slug>/chapters/<int:chapter_number>/add-author-note/', views.add_author_note, name='add_author_note'),
    path('<slug:slug>/chapters/<int:chapter_number>/edit-author/', views.edit_author_note, name='edit_author_note'),
    path('<slug:slug>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<slug:slug>/delete/', views.delete_novel, name='delete_novel'),
    path('<slug:slug>/comment/', views.add_novel_comment, name='add_novel_comment'),
    path('novel_comment/<int:comment_id>/delete/', views.delete_novel_comment, name='delete_novel_comment'),
    path('<slug:slug>/rate/', views.rate_novel, name='rate_novel'),
    path('<slug:slug>/toggle-follow/', views.toggle_follow, name='toggle_follow'),
    path('follows/', views.followed_novels, name='followed_novels'),
]