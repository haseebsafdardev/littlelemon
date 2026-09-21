from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from restaurant.models import Booking, Menu


class CapstoneProjectTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="reviewer", password="StrongPass123!"
        )
        self.token = Token.objects.create(user=user)
        self.client = APIClient()

    def test_menu_endpoint(self):
        Menu.objects.create(title="Hummus", price="8.00", inventory=20)
        response = self.client.get("/api/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], "Hummus")

    def test_booking_endpoint(self):
        Booking.objects.create(
            first_name="Alex",
            reservation_date=date(2026, 9, 21),
            reservation_slot=19,
        )
        response = self.client.get("/api/bookings/?date=2026-09-21")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
