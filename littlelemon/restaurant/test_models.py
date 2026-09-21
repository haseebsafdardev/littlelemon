from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Booking, Menu


class CapstoneAPITests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="StrongPass123!"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_menu_get(self):
        Menu.objects.create(title="Greek Salad", price="12.50", inventory=10)
        response = self.client.get("/api/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], "Greek Salad")

    def test_booking_create_requires_authentication(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "first_name": "Guest",
                "reservation_date": "2026-09-21",
                "reservation_slot": 18,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_booking_create_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            "/api/bookings/",
            {
                "first_name": "Guest",
                "reservation_date": "2026-09-21",
                "reservation_slot": 18,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_date_filter(self):
        Booking.objects.create(
            first_name="Test",
            reservation_date=date(2026, 9, 21),
            reservation_slot=10,
        )
        response = self.client.get("/api/bookings/?date=2026-09-21")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
