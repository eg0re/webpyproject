from django.urls import path
from . import views

urlpatterns = {
    path('', views.ShoeboxListView.as_view(), name='box-list'),
    path('show/<int:pk>/', views.ShoeboxDetailView.as_view(), name='box-detail'),
}