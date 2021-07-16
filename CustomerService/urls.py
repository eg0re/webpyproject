from django.urls import path
from . import views
from Shoebox.views import ShoeboxCreate

urlpatterns = [
    path('delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('edit/<int:pk>/', views.comment_edit, name='comment-edit'),
    path('reports/', views.CommentReportView.as_view(), name='comment-reports'),
    path('add/', ShoeboxCreate.as_view(), name="box-create"),
    path('boxedit/<int:pk>', views.editBox, name="box-edit"),
]
