from django.contrib import admin
from .models import Poll, Vote

# Register your models here.
class PollAdmin(admin.ModelAdmin):
    list_display = ['user', 'vote_a_count', 'vote_b_count', 'created_time', 'media_a', 'media_b']
    list_filter = ['created_time']


admin.site.register(Poll, PollAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'poll', 'choice', 'created_time']
    list_filter = ['created_time']


admin.site.register(Vote, VoteAdmin)
