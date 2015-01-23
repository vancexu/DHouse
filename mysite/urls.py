from django.conf.urls import patterns, include, url
from django.contrib import admin

from mysite.views import *
#from mysite.views import index, register, signin, signout, profile
#from mysite.view import buy, changeProfile, productsAvaliable, productsall, order

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^charts/', charts),

    url(r'^$', index, name="index"),
    url(r'^register/$', register),
    url(r'^signin/$', signin),
    url(r'^signout/$', signout),
    url(r'^profile/?$', profile),
    url(r'^profile/(?P<user_id>\d+)/?$', profile),
    url(r'^buy/?$', buy),
    url(r'^buy/(?P<product_id>\d+)/?$', buy),
    url(r'^change/(?P<profile_id>\d+)/?$', changeProfile),
    url(r'^productsavaliable/?$', productsAvaliable),
    url(r'^productsall/?$', productsAll),
    url(r'^order/?$', order),
    url(r'^order/(?P<product_id>\d+)/?$', order),
    url(r'^confirmorder/(?P<order_id>\d+)/?$', confirmOrder),
    url(r'^cancelorder/(?P<order_id>\d+)/?$', cancelOrder),
    url(r'^contact/?$', contact),

)
