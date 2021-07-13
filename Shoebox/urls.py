from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShoeboxListView.as_view(), name='box-list'),
    path('box/<int:bpk>/', views.shoebox_detail, name='box-detail'),
    path('add/', views.ShoeboxCreateView.as_view(), name="box-create"),
    path('<int:pk>/<str:up_or_down>/', views.vote, name='comment-vote'),
    path('box/<int:pk>/delete/', views.ShoeboxDeleteView.as_view(), name='box-delete'),
    path("search/", views.box_search, name="box_search")
]