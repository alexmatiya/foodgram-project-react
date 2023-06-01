from django.urls import include, path
from rest_framework.routers import DefaultRouter


v1 = DefaultRouter()

urlpatterns = [
    path('', include(v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
