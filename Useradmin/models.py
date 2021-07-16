from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import Shoppingcart


def get_myuser_from_user(user):
    myuser = None
    myuser_query_set = MyUser.objects.filter(user=user)
    if len(myuser_query_set) > 0:
        myuser = myuser_query_set.first()
    return myuser


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def is_staff(self):
        if self.user.is_staff or self.user.is_superuser:
            return True
        else:
            return False

    def get_profile_path(self):
        return self.profile_picture.url

    def get_username(self):
        return self.user.username

    def execute_after_login(self):
        print(self.__str__())
        self.save()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + str(self.user.username) + ')'
