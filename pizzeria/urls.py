from django.urls import path, include
from pizzeria.views import (
    OrderView,
    OrderItemViewSet,
    PlaceOrderView,
    PizzaViewSet,
    CategoryViewSet,
    ItemViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"orderitem", OrderItemViewSet)
router.register(r"pizza", PizzaViewSet)
router.register(r"cateogry", CategoryViewSet)
router.register(r"item", ItemViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("order/", OrderView.as_view(), name="review your order"),
    path("order/place-order/", PlaceOrderView.as_view(), name="place your order"),
]
