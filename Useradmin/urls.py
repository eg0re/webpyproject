from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.MySignUp.as_view(), name='signup'),
    path("list/", views.MyUserList.as_view(), name="user-list"),
    path("login/", views.MyLogin.as_view(), name="login")
]
