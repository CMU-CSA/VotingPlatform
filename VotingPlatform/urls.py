from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'VotingPlatform.views.home', name='home'),
    url(r'^index$', 'VotingPlatform.views.login_index', name='index'),
    url(r'^round1$', 'VotingPlatform.views.round1', name='round1'),
    url(r'^round2$', 'VotingPlatform.views.round2', name='round2'),
    url(r'^vote$', 'VotingPlatform.views.vote', name='vote'),
    url(r'^manage$', 'VotingPlatform.views.admin_page', name='manage'),
    url(r'^edit_candidate_page/(?P<cid>\d+)$', 'VotingPlatform.views.edit_candidate_page', name='edit_candidate_page'),
    url(r'^edit_confirm$', 'VotingPlatform.views.edit_candidate', name='edit_candidate'),
    url(r'^remove$', 'VotingPlatform.views.remove_candidate', name='remove'),
    url(r'^add$', 'VotingPlatform.views.add_candidate', name='add'),
    url(r'^login$', 'VotingPlatform.views.user_login', name='login'),
    url(r'^logout$', 'VotingPlatform.views.user_logout', name='logout'),
    url(r'^pair$', 'VotingPlatform.views.pair_candidates', name='pair'),
    url(r'^unpair$', 'VotingPlatform.views.unpair_candidates', name='unpair'),
    url(r'^photo/(?P<cid>\d+)$', 'VotingPlatform.views.get_photo', name='photo'),
    url(r'^remove_picture$', 'VotingPlatform.views.remove_picture', name='remove_picture'),
    url(r'^nextround$', 'VotingPlatform.views.next_round', name='next_round'),
    url(r'^prevround$', 'VotingPlatform.views.prev_round', name='prev_round'),
    url(r'^enable$', 'VotingPlatform.views.enable_voting', name='enable_voting'),
    url(r'^disable$', 'VotingPlatform.views.disable_voting', name='disable_voting'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
