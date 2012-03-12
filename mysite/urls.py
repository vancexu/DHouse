from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('dhouse.views',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^charts/', 'charts'),
    url(r'^$', 'index'),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^register/$', 'register'),
    url(r'^signin/$', 'signin'),
    url(r'^signout/$', 'signout'),
    url(r'^profile/?$', 'profile'),
    url(r'^profile/(?P<user_id>\d+)/?$', 'profile'),
    url(r'^buy/?$', 'buy'),
    url(r'^buy/(?P<product_id>\d+)/?$', 'buy'),
    url(r'^change/(?P<profile_id>\d+)/?$', 'changeProfile'),
    url(r'^productsavaliable/?$', 'productsAvaliable'),
    url(r'^productsall/?$', 'productsAll'),
    url(r'^order/?$', 'order'),
    url(r'^order/(?P<product_id>\d+)/?$', 'order'),
    url(r'^confirmorder/(?P<order_id>\d+)/?$', 'confirmOrder'),
    url(r'^cancelorder/(?P<order_id>\d+)/?$', 'cancelOrder'),
    url(r'^contact/?$', 'contact'),
)
