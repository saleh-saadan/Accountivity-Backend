from django.contrib import admin

# Register your models here.

from .models import User, Friendships

admin.site.register(User)
admin.site.register(Friendships)
