from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('command.urls')),
    path('', include('message.urls')),
    path('', include('product.urls')),
]
