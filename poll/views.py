from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from .models import Poll,Vote
from user.models import Profile, Follow
from .forms import PollCreateForm
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.forms import Textarea

import json
import urllib3

# Create your views here.
def list(request):
    try:
        user = request.user
        if user.is_anonymous:
            return HttpResponseRedirect(reverse('index'))
        else:
            instagram_login = user.social_auth.get(provider='instagram')
    except UserSocialAuth.DoesNotExist:
        instagram_login = None

    voted_polls = Vote.objects.filter(user=user).values_list('poll',  flat=True)
    follows = Follow.objects.filter(user=user).values_list('follows', flat=True)
    print(follows)

    latest_poll_list = Poll.objects.order_by('-created_time')[:5]
    context = {
        'instagram_login': instagram_login,
        'latest_poll_list': latest_poll_list,
        'voted_polls': voted_polls,
        'follows': follows,
    }

    return render(request, 'poll/list.html', context)

# new upload to s3
class PollCreateView(CreateView):
    model = Poll
    fields = ['media_a', 'media_b', 'caption']
    widgets = {
        'caption': Textarea(attrs={'cols': 80, 'rows': 5}),
    }

    success_url = reverse_lazy('poll:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PollCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Poll.objects.all()
        context['poll'] = documents
        return context

@login_required
def poll_vote(request, id, choice):

    print("VOTE BUTTON PRESSED")
    print(request.method)
    print(request.is_ajax())
    print("id: %s, choice: %s" % (id, choice))

    user = request.user
    poll = Poll.objects.get(pk=id)
    voted, created = Vote.objects.get_or_create(user=user, poll=poll)

    if created:
        if choice == 'a':
            poll.vote_a_count += 1
            voted.choice = 'a'
        else:
            poll.vote_b_count += 1
            voted.choice = 'b'
        voted.save()
        poll.save()
    else:
        pass

    voted_polls = Vote.objects.filter(user=user).values_list('poll',  flat=True)

    try:
        user = request.user
        if user.is_anonymous:
            instagram_login = None
        else:
            instagram_login = user.social_auth.get(provider='instagram')
    except UserSocialAuth.DoesNotExist:
        instagram_login = None

    latest_poll_list = Poll.objects.order_by('-created_time')[:5]
    context = {
        'instagram_login': instagram_login,
        'latest_poll_list': latest_poll_list,
        'voted_polls': voted_polls,
    }

    print("before calling ajax if")
    if request.is_ajax():
        print("This is AJAX")
        data = json.dump(context)
        return HttpResponse(data, content_type='application/json')

    return render(request, 'poll/list.html', context)

@login_required
def poll_detail(request, id):

    try:
        poll = Poll.objects.get(pk=id)
        profile_user = poll.user
        profile = Profile.objects.get(user=profile_user)

    except Poll.DoesNotExist:
        poll = None
        return HttpResponseRedirect(reverse('poll:list'))

    try:
        user = request.user
        if user.is_anonymous:
            return HttpResponseRedirect(reverse('index'))
        else:
            instagram_login = user.social_auth.get(provider='instagram')

        voted_polls = Vote.objects.filter(user=user).values_list('poll',  flat=True)
        follows = Follow.objects.filter(user=user).values_list('follows', flat=True)
        profile_follows = Follow.objects.filter(user=profile_user).values_list('follows', flat=True)
        print(follows)

    except UserSocialAuth.DoesNotExist:
        instagram_login = None

    latest_poll_list = Poll.objects.filter(pk=id).order_by('-created_time')[:5]
    context = {
        'instagram_login': instagram_login,
        'latest_poll_list': latest_poll_list,
        'voted_polls': voted_polls,
        'follows': follows,
        'profile': profile,
        'profile_follows': profile_follows,
    }

    return render(request, 'poll/detail.html', context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PollVoteAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None, choice=None, format=None):
        user = request.user
        poll = Poll.objects.get(pk=id)
        voted, created = Vote.objects.get_or_create(user=user, poll=poll)

        print("POLL VOTE API CALLED!!")
        if created:
            if choice == 'a':
                poll.vote_a_count += 1
                voted.choice = 'a'
            else:
                poll.vote_b_count += 1
                voted.choice = 'b'
            voted.save()
            poll.save()
        else:
            pass

        data = {
            "vote_a_count": poll.vote_a_count,
            "vote_b_count": poll.vote_b_count
        }
        return Response(data)
