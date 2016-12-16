from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from blog.models import Post, Comment, BlogUser

# Register your models here.


class BlogUserInline(admin.StackedInline):
    model = BlogUser
    can_delete = False
    verbose_name_plural = 'blog_users'


class UserAdmin(BaseUserAdmin):
    inlines = (BlogUserInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)