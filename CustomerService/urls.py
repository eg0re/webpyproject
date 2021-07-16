from django.urls import path
from . import views

urlpatterns = [
    path('delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('edit/<int:pk>/', views.comment_edit, name='comment-edit'),
]
