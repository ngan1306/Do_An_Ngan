from django.urls import path, include
from . import views

urlpatterns = [
    path('chapter/<slug:slug>/<int:chapter_number>/', views.chapter_detail, name='chapter_detail'),
    path('chapter/<slug:slug>/<int:chapter_number>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('<slug:slug>/comment/', views.add_novel_comment, name='add_novel_comment'),
    path('novel_comment/<int:comment_id>/delete/', views.delete_novel_comment, name='delete_novel_comment'),
    path('api/', include('novels.api_urls')),
] 