from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'wallet.views.dashboard_view', name='home'),
    url(r'^addmoney$', 'wallet.views.add_money_to_wallet', name='addmoney'),
    url(r'^transfer$', 'wallet.views.transfer', name='transfer'),
    url(r'^passbook$', 'wallet.views.passbook', name='passbook'),
    url(r'^login$', 'wallet.views.login_view', name='login'),
    url(r'^signup$', 'wallet.views.signup_view', name='signup'),
    url(r'^admin/', include(admin.site.urls)),
]
