from django.contrib import admin
from .models import Profile, Follow

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_id', 'full_name']

admin.site.register(Profile, ProfileAdmin)

class FollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'follows', 'added']

admin.site.register(Follow, FollowAdmin)
