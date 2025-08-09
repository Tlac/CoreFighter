from rest_framework.routers import DefaultRouter
from .views import DeckListViewSet

router = DefaultRouter()
router.register(r"", DeckListViewSet, basename="deck")

urlpatterns = router.urls
