from django.conf.urls import patterns, url
from pubcrawl import views

urlpatterns = patterns('',
    url(r'^$', views.welcome, name='welcome'),
	url(r'^index/$', views.index, name='index'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^search/$', views.search, name='search'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^add_profile/$', views.register_profile, name='add_profile'),
    url(r'^profile/(?P<profile_user_name>[\w\-]+)/(?P<pageContent>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^account_details/(?P<profile_user_name>[\w\-]+)/$', views.account_details, name='account_details'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^profile_list/$', views.profile_list, name='profile_list'),
    url(r'^create_pubcrawl/$', views.create_pubcrawl, name='create_pubcrawl'),
    url(r'^crawl/(?P<crawl_name>[\w\-]+)/$', views.crawl, name='crawl'),
	url(r'^rate_crawl/$', views.rate_crawl, name='rate_crawl'),
	url(r'^crawl_list/$', views.crawl_list, name='crawl_list'),
    url(r'^results/$', views.results, name='results'),
    url(r'^results/(?P<search_tag>[\w\-]+)/$', views.results, name='search')
    ) 


