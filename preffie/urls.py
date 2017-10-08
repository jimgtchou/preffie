"""preffie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from user import views as core_views


urlpatterns = [
    url(r'^$', core_views.index, name='index'),
    url(r'^privacy/$', core_views.privacy, name='privacy'),
    # url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout,name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    # url(r'^admin/', admin.site.urls),

    # url(r'^$',views.index,name='index'),
    # url(r'^special/',views.special,name='special'),
    url(r'^admin/', admin.site.urls),
    url(r'^user/',include('user.urls')),
    url(r'^poll/',include('poll.urls')),
    # url(r'^logout/$', views.user_logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
