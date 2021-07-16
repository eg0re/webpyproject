from django.contrib import admin

# Register your models here.
import Useradmin.models

admin.site.register(Useradmin.models.MyUser)