from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, TagViewSet, RecipeViewSet,
                       UserSubscribeView, UserSubscriptionsViewSet)

v1 = DefaultRouter()

v1.register(r'tags', TagViewSet, basename='tags')
v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
v1.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('users/subscriptions/',
         UserSubscriptionsViewSet.as_view({'get': 'list'})),
    path('users/<int:user_id>/subscribe/', UserSubscribeView.as_view()),
    path('', include(v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
