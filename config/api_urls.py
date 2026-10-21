"""REST API routes. Register new viewsets here."""
from rest_framework.routers import DefaultRouter

from apps.catalog.api import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")

urlpatterns = router.urls
