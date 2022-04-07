from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('subscribed_at', )


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
