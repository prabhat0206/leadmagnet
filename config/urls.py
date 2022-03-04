from django.contrib import admin
from django.urls import path, include
from vendor.views import LoginToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('rest/calls/', include('callcenter.urls')),
    path('rest/vendor/', include('vendor.urls')),
    path('rest/auth/login', LoginToken.as_view(), name='login'),
]
