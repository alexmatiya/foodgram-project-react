from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TagViewSet
      

v1 = DefaultRouter()

v1.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
