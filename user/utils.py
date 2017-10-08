from .models import Profile, Follow
from poll.models import Poll, Vote
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth

import urllib3
import json

def create_profile(strategy, details, response, user, *args, **kwargs):
    if Profile.objects.filter(user=user).exists():
        data = response.get('data')
        my_profile = Profile.objects.filter(user=user)[0]
        my_profile.username = data.get('username')
        my_profile.profile_picture_url = data.get('profile_picture')
        my_profile.full_name = data.get('full_name')
        my_profile.bio = data.get('bio')
        my_profile.website = data.get('website')
        my_profile.is_business = data.get('is_business')
        my_profile.media_count = Poll.objects.filter(user=user).count()
        my_profile.follows_count = Follow.objects.filter(user=user).count()
        my_profile.followed_by_count = data.get('counts').get('followed_by')
        my_profile.save()
    else:
        # pass
        data = response.get('data')
        new_profile = Profile(user=user)
        new_profile.userid = data.get('id')
        new_profile.username = data.get('username')
        new_profile.profile_picture_url = data.get('profile_picture')
        new_profile.full_name = data.get('full_name')
        new_profile.bio = data.get('bio')
        new_profile.website = data.get('website')
        new_profile.is_business = data.get('is_business')
        new_profile.media_count = 0
        new_profile.follows_count = 0
        new_profile.followed_by_count = data.get('counts').get('followed_by')
        new_profile.save()
    return kwargs


# need to make follow its own entity (between user profiles)
def update_relationships(strategy, details, response, user, *args, **kwargs):
    access_token= response.get('access_token')
    try:
        profile = Profile.objects.filter(user=user)[0]
        http = urllib3.PoolManager()
        url = 'https://api.instagram.com/v1/users/self/follows?access_token={}'.format(access_token)
        follows_response = http.request('GET', url)
        follows_data = json.loads(follows_response.data.decode('utf-8'))
        ig_follows_list = follows_data.get('data')
        ig_follows_list_id = [float(x.get('id')) for x in ig_follows_list]
        # tuple of id current user is following on instagram
        ig_follows_list_tup = tuple(ig_follows_list_id)
        # list of follows user id that is on Preffie
        on_preffie_list = Profile.objects.filter(userid__in=ig_follows_list_tup).values_list('userid', flat=True)
        # list of follows profile_id already follow on preffie
        preffie_follows_list_id = Follow.objects.filter(user=user).values_list('follows', flat=True)
        to_delete_profiles = []
        for x in preffie_follows_list_id:
            to_delete_profiles.append(int(x))

        if ig_follows_list:
            if on_preffie_list:
                for ig_follows in ig_follows_list:
                    ig_follows_id = float(ig_follows.get('id'))
                    if ig_follows_id in on_preffie_list:
                        temp_profile, created= Profile.objects.get_or_create(userid=ig_follows_id)
                        if not created:
                            in_profile = False
                            in_profile = temp_profile.id in preffie_follows_list_id
                            temp_profile.username = ig_follows.get('username')
                            temp_profile.full_name = ig_follows.get('full_name')
                            temp_profile.profile_picture_url = ig_follows.get('profile_picture')
                            temp_profile.save()
                            if temp_profile.id in preffie_follows_list_id:
                                to_delete_profiles.remove(int(temp_profile.id))
                            # if temp_profile in preffie_follows_list_id:
                            ### add to query set
                            elif not Follow.objects.filter(user=user, follows=temp_profile).exists():
                                new_follow = Follow(user=user, follows=temp_profile)
                                new_follow.save()
        if to_delete_profiles:
            print("going into unfollow loop to_delete_profile: %s" % to_delete_profiles)
            for unfollowed_profile_id in to_delete_profiles:
                temp_profile, created= Profile.objects.get_or_create(id=unfollowed_profile_id)
                if not created:
                    temp_follow = Follow.objects.get(user=user, follows=temp_profile)
                    temp_follow.delete()

    except UserSocialAuth.DoesNotExist:
        print('User not exist')
        instagram_login = None

    return kwargs
