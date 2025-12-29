from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Category, Location, Post, Comment

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Post)
admin.site.register(Comment)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)