from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.product.views import ProductModelViewSet
from api.v1.establishment.views import EstablishmentModelViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns.extend(
    [
        # product
        path("product/", ProductModelViewSet.as_view({"get": "list"}), name="product-list"),
        path("product/create/", ProductModelViewSet.as_view({"post": "create"}), name="product-create"),
        path("product/update/<pk>/", ProductModelViewSet.as_view({"put": "update"}), name="product-update"),
        path("product/delete/<pk>/",ProductModelViewSet.as_view({"delete": "delete"}), name="product-delete"),

        # Establishment
        path("establishment/", EstablishmentModelViewSet.as_view({"get": "list"}), name="establishment-list"),
        path("establishment/create/", EstablishmentModelViewSet.as_view({"post": "create"}), name="establishment-create"),
        path("establishment/update/<uuid:pk>/", EstablishmentModelViewSet.as_view({"put": "update"}), name="establishment-update"),
        path("establishment/delete/<uuid:pk>/",EstablishmentModelViewSet.as_view({"delete": "delete"}), name="establishment-delete"),
    ]
)