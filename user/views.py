from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from social_django.models import UserSocialAuth
from user.models import Profile, Follow
from poll.models import Poll, Vote
from django.contrib.auth.models import User


import urllib
import json

# Create your views here.
def index(request):
    user = request.user

    try:
        instagram_login = user.social_auth.get(provider='instagram')
    except UserSocialAuth.DoesNotExist:
        instagram_login = None
    except:
        instagram_login = None

    return render(request,'user/index.html', {'instagram_login': instagram_login})


def privacy(request):
    user = request.user

    try:
        instagram_login = user.social_auth.get(provider='instagram')
    except UserSocialAuth.DoesNotExist:
        instagram_login = None
    except:
        instagram_login = None

    return render(request,'user/privacy.html', {'instagram_login': instagram_login})


@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

@login_required
def button_pressed(request):
    # Log out the user.
    print('the button has been pressed')

    user = request.user

    try:
        instagram_login = user.social_auth.get(provider='instagram')
        access_token = instagram_login.extra_data.get('access_token')
        print('access token: %s' % access_token)
        http = urllib3.PoolManager()
        url = 'https://api.instagram.com/v1/users/self/?access_token={}'.format(access_token)
        response = http.request('GET', url)
        print(response.data.decode('utf-8'))
    except UserSocialAuth.DoesNotExist:
        print('User not exist')
        instagram_login = None

    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

@login_required
def profile(request):
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

    latest_poll_list = Poll.objects.filter(user=user).order_by('-created_time')[:5]
    context = {
        'instagram_login': instagram_login,
        'latest_poll_list': latest_poll_list,
        'voted_polls': voted_polls,
        'follows': follows,
    }

    return render(request, 'user/profile.html', context)

@login_required
def profile_view(request, id):

    profile_user = User.objects.get(pk=id)

    profile = Profile.objects.get(user=profile_user)

    try:
        user = request.user
        if user.is_anonymous:
            return HttpResponseRedirect(reverse('index'))
        elif user == profile_user:
            return HttpResponseRedirect(reverse('user:profile'))
        else:
            instagram_login = user.social_auth.get(provider='instagram')

        access_token = instagram_login.extra_data.get('access_token')
        print('access token: %s' % access_token)
        http = urllib3.PoolManager()
        url = 'https://api.instagram.com/v1/users/{}/?access_token={}'.format(str(profile.userid).rstrip('.0'),access_token)
        response = http.request('GET', url)
        data = json.loads(response.data.decode('utf-8')).get('data')

        profile.username = data.get('username')
        profile.profile_picture_url = data.get('profile_picture')
        profile.full_name = data.get('full_name')
        profile.bio = data.get('bio')
        profile.website = data.get('website')
        profile.is_business = data.get('is_business')
        profile.media_count = Poll.objects.filter(user=profile_user).count()
        profile.follows_count = Follow.objects.filter(user=profile_user).count()
        profile.followed_by_count = data.get('counts').get('followed_by')
        profile.save()

    except UserSocialAuth.DoesNotExist:
        instagram_login = None

    voted_polls = Vote.objects.filter(user=user).values_list('poll',  flat=True)
    follows = Follow.objects.filter(user=user).values_list('follows', flat=True)
    profile_follows = Follow.objects.filter(user=profile_user).values_list('follows', flat=True)
    print(follows)

    latest_poll_list = Poll.objects.filter(user=profile_user).order_by('-created_time')[:5]
    context = {
        'instagram_login': instagram_login,
        'latest_poll_list': latest_poll_list,
        'voted_polls': voted_polls,
        'follows': follows,
        'profile': profile,
        'profile_follows': profile_follows,
    }

    return render(request, 'user/profile_view.html', context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class FollowAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None, format=None):
        user = request.user
        to_follow_profile = Profile.objects.get(user=id)
        to_follow_name = to_follow_profile.username

        try:
            instagram_login = user.social_auth.get(provider='instagram')
            access_token = instagram_login.extra_data.get('access_token')
            http = urllib3.PoolManager()
            url = 'https://api.instagram.com/v1/users/{}/relationship?access_token={}'.format(str(to_follow_profile.userid).rstrip('.0'),access_token)
            get_response = http.request('GET', url)
            relationship_data = json.loads(get_response.data.decode('utf-8'))
            outgoing_status = relationship_data.get('data').get('outgoing_status')
            is_following = False

            if str(outgoing_status) == 'none':
                print("follow called")
                data = {"action":"follow"}
                post_response = http.request('POST', url, fields=data)
                post_data = json.loads(post_response.data.decode('utf-8'))
                outgoing_status = post_data.get('data').get('outgoing_status')

                followed, created = Follow.objects.get_or_create(user=user, follows=to_follow_profile)
                if created:
                    followed.save()

                if str(outgoing_status) == 'follows':
                    is_following = True
            elif outgoing_status == 'follows':
                print("unfollow called")
                data = {"action":"unfollow"}
                post_response = http.request('POST', url, fields=data)
                post_data = json.loads(post_response.data.decode('utf-8'))
                outgoing_status = post_data.get('data').get('outgoing_status')

                followed, created = Follow.objects.get_or_create(user=user, follows=to_follow_profile)
                if not created:
                    followed.delete()

                if outgoing_status == 'none':
                    is_following = False

        except UserSocialAuth.DoesNotExist:
            print('User not exist')
            instagram_login = None

        print(is_following)

        data = {
            "follow_status": is_following,
            "profile_username": to_follow_name,
        }

        return Response(data)
