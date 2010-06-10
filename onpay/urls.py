from django.conf.urls.defaults import *

urlpatterns = patterns('onpay.views',
    url(r'^fill/$', 'process_first_step', name='onpay_fill'),
    url(r'^api/$', 'process_api_request', name='onpay_api' ),
)
