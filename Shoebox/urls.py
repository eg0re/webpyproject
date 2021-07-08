from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShoeboxListView.as_view(), name='box-list'),
    path('box/<int:pk>/', views.shoebox_detail, name='box-detail'),
    path('add/', views.ShoeboxCreateView.as_view(), name="box-create"),
    path('box/<int:pk>/delete/', views.ShoeboxDeleteView.as_view(), name='box-delete'),
]