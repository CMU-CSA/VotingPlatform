from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'VotingPlatform.views.home', name='home'),
    url(r'^voting$', 'VotingPlatform.views.voting_page', name='voting_page'),
    url(r'^vote$', 'VotingPlatform.views.vote', name='vote'),
    url(r'^manage$', 'VotingPlatform.views.admin_page', name='manage'),
    url(r'^remove$', 'VotingPlatform.views.remove_candidate', name='remove'),
    url(r'^add$', 'VotingPlatform.views.add_candidate', name='add'),
    url(r'^login$', 'VotingPlatform.views.user_login', name='login'),
    url(r'^pair$', 'VotingPlatform.views.pair_candidates', name='pair'),
    url(r'^unpair$', 'VotingPlatform.views.unpair_candidates', name='unpair'),
    url(r'^photo/(?P<cid>\d+)$', 'VotingPlatform.views.get_photo', name='photo'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
