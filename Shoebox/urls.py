from django.urls import path

import Shoppingcart.views
from . import views

urlpatterns = [
    path('', views.ShoeboxListView.as_view(), name='box-list'),
    path('box/<int:bpk>/', views.shoebox_detail, name='box-detail'),
    path('basket/<int:bpk>/', Shoppingcart.views.basket, name='basket'),
    path('mybasket/', Shoppingcart.views.show_shopping_cart, name='mybasket'),
    path('add/', views.ShoeboxCreate.as_view(), name="box-create"),
    path('<int:commentid>/<str:up_or_down>/', views.vote, name='comment-vote'),
    path('report/<int:commentid>/', views.comment_report, name='comment-report'),
    path('pdfdl/<int:pk>', views.pdfdl, name='pdfdl'),
    path('box/<int:pk>/delete/', views.ShoeboxDeleteView.as_view(), name='box-delete'),
    path("search/", views.box_search, name="box_search")
]