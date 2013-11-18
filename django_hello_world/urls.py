from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django_hello_world.hello.views.home', name='home'),
    url(r'^requests/$', 'django_hello_world.hello.views.latest_requests', name='latest_requests'),
    url(r'^edit/$', 'django_hello_world.hello.views.edit_home', name='edit_home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'})
)
