from django.conf.urls import url
from poll import views
from user import views as user_view
from django.contrib.auth.decorators import login_required

# SET THE NAMESPACE!
app_name = 'poll'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    # url(r'^index/$', views.index,name='index'),
    url(r'^$', views.list,name='list'),
    url(r'^create/$', login_required(views.PollCreateView.as_view()),name='create'),
    url(r'^detail/(?P<id>\d+)/$', views.poll_detail, name='detail'),
    url(r'^(?P<id>\d+)/vote/(?P<choice>\w+)/$', views.poll_vote, name='vote'),
    url(r'^api/(?P<id>\d+)/vote/(?P<choice>\w+)/$', views.PollVoteAPI.as_view(), name='vote-api'),
]
