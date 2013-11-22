from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'hello.views.home', name='home'),
    url(r'^requests/$', 'hello.views.latest_requests', name='latest_requests'),
    url(r'^edit/$', 'hello.views.edit_home', name='edit_home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'})
)

if settings.DEBUG:
    # Media for debug
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
    # Static for debug
    urlpatterns += staticfiles_urlpatterns()
