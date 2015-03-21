from django.conf.urls import patterns, url
from pubcrawl import views

urlpatterns = patterns('',
    url(r'^$', views.welcome, name='welcome'),
	url(r'^index/$', views.index, name='index'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    #url(r'^register/$', views.register, name='register'),
    #url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    #url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^search/$', views.search, name='search'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^add_profile/$', views.register_profile, name='add_profile'),
    url(r'^profile/(?P<profile_user_name>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^profile_list/$', views.profile_list, name='profile_list'),
    url(r'^create_pubcrawl/$', views.create_pubcrawl, name='create_pubcrawl'),
    ) 


