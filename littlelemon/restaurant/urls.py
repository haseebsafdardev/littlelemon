from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .api_views import BookingViewSet, MenuViewSet

router = DefaultRouter()
router.register(r"menu", MenuViewSet, basename="menu")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path("", views.home, name="home"),
    path("book/", views.book, name="book"),
    path("reservations/", views.reservations, name="reservations"),
    path("bookings", views.bookings, name="bookings"),
    path("api/", include(router.urls)),
]
