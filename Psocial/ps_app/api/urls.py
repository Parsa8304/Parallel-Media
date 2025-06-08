from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, PersonaViewSet, ClashViewSet, UniverseMergeViewSet
from .views import RegisterView



router = routers.SimpleRouter()
router.register('posts', PostViewSet)
router.register('personas', PersonaViewSet)
router.register('clashes', ClashViewSet)
router.register('universe-merges', UniverseMergeViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]

