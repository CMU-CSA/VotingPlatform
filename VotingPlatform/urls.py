from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^index$', views.login_index, name='index'),
    url(r'^round1$', views.round1, name='round1'),
    url(r'^round2$', views.round2, name='round2'),
    url(r'^vote$', views.vote, name='vote'),
    url(r'^manage$', views.admin_page, name='manage'),
    url(r'^edit_candidate_page/(?P<cid>\d+)$', views.edit_candidate_page, name='edit_candidate_page'),
    url(r'^edit_confirm$', views.edit_candidate, name='edit_candidate'),
    url(r'^remove$', views.remove_candidate, name='remove'),
    url(r'^add$', views.add_candidate, name='add'),
    url(r'^login$', views.user_login, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    #url(r'^pair$', views.pair_candidates', name='pair'),
    #url(r'^unpair$', views.unpair_candidates', name='unpair'),
    url(r'^photo/(?P<cid>\d+)$', views.get_photo, name='photo'),
    url(r'^remove_picture$', views.remove_picture, name='remove_picture'),
    url(r'^nextround$', views.next_round, name='next_round'),
    url(r'^prevround$', views.prev_round, name='prev_round'),
    url(r'^enable$', views.enable_voting, name='enable_voting'),
    url(r'^disable$', views.disable_voting, name='disable_voting'),
    url(r'^clear_records', views.clear_records, name='clear_records'),
    url(r'^a_random_page_that_probably_does_not_exist$', views.troll, name='troll'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^display$',views.display, name='display'),
    url(r'^displayData',views.displayData, name='displayData'),
    url(r'^add_andrewids',views.add_andrewids, name='add_andrewids'),
    url(r'^admin/', include(admin.site.urls)),
]
