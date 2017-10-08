from django.conf.urls import url
from user import views

# SET THE NAMESPACE!
app_name = 'user'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^index/$',views.index,name='index'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^profile/(?P<id>\w+)/$',views.profile_view,name='profile_view'),
    url(r'^logout/$',views.signout ,name='logout'),
    url(r'^button_pressed/$',views.button_pressed,name='button_pressed'),
    url(r'^api/(?P<id>\w+)/follow/$', views.FollowAPI.as_view(), name='follow-api'),
]
