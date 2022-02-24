from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('rest/calls/', include('callcenter.urls')),
    path('rest/auth/login', obtain_auth_token, name='login'),
]
