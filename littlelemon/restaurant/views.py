from datetime import date

from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_http_methods

from .forms import BookingForm
from .models import Booking


def home(request):
    return render(request, "home.html")


@require_http_methods(["GET", "POST"])
def book(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
            except IntegrityError:
                form.add_error(
                    "reservation_slot",
                    "That time is already booked for the selected date.",
                )
            else:
                return redirect("book")
    else:
        form = BookingForm(initial={"reservation_date": date.today()})

    return render(request, "book.html", {"form": form})


@require_GET
def reservations(request):
    bookings = Booking.objects.all()
    data = [
        {
            "model": "restaurant.booking",
            "pk": booking.pk,
            "fields": {
                "first_name": booking.first_name,
                "reservation_date": booking.reservation_date.isoformat(),
                "reservation_slot": booking.reservation_slot,
            },
        }
        for booking in bookings
    ]
    return JsonResponse(data, safe=False)


@require_GET
def bookings(request):
    requested_date = request.GET.get("date")
    queryset = Booking.objects.all()

    if requested_date:
        try:
            selected = date.fromisoformat(requested_date)
        except ValueError:
            return JsonResponse(
                {"error": "Invalid date. Use YYYY-MM-DD."},
                status=400,
            )
        queryset = queryset.filter(reservation_date=selected)

    data = [
        {
            "model": "restaurant.booking",
            "pk": booking.pk,
            "fields": {
                "first_name": booking.first_name,
                "reservation_date": booking.reservation_date.isoformat(),
                "reservation_slot": booking.reservation_slot,
            },
        }
        for booking in queryset
    ]
    return JsonResponse(data, safe=False)


from .api_views import MenuViewSet, BookingViewSet
