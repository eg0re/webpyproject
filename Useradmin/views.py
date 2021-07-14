from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from Useradmin.forms import MySignUpForm
from django.urls import reverse_lazy
from django.views import generic
from Useradmin.models import MyUser
from django.contrib.auth.models import User
from django.contrib.auth import (
    login as auth_login
)


class MySignUp(generic.CreateView):
    form_class = MySignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        print("VALID")
        data = form.cleaned_data
        user = User.objects.create_user(username=data["username"],
                                        password=data["password"],
                                        first_name=data["first_name"],
                                        last_name=data["last_name"],
                                        email=data["email"])
        my_user = MyUser.objects.create(user=user,
                                        profile_picture=data["profile_picture"])
        return redirect("login")


class MyUserList(generic.ListView):
    model = MyUser
    context_object_name = "all_myusers"
    template_name = "myuser-list.html"


class MyLogin(LoginView):
    template_name = "registration/login.html"

    def form_valid(self, form):
        """Security check complete. Log the user in. PERFORM CUSTOM CODE."""
        auth_login(self.request, form.get_user())

        # execute_after_login() is in MyUser class
        # If there is a MyUser object behind the User object,
        # access it and call execute_after_login()
        user = form.get_user()  # Class is User, not MyUser
        # print('-------------', user.__class__.__name__)
        #myuser = get_myuser_from_user(user)
        #if myuser is not None:
            #myuser.execute_after_login()  # Custom code
        return HttpResponseRedirect(self.get_success_url())

