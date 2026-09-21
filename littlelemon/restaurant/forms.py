from django import forms
from .models import Booking

TIME_SLOTS = [(hour, f"{hour % 12 or 12} {'AM' if hour < 12 else 'PM'}") for hour in range(10, 21)]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["first_name", "reservation_date", "reservation_slot"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "Your Name", "autocomplete": "name"}
            ),
            "reservation_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "reservation_slot": forms.Select(choices=TIME_SLOTS),
        }

    def clean_first_name(self):
        value = self.cleaned_data["first_name"].strip()
        if not value:
            raise forms.ValidationError("Please enter your name.")
        return value

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get("reservation_date")
        slot = cleaned.get("reservation_slot")
        if date and slot is not None:
            qs = Booking.objects.filter(
                reservation_date=date,
                reservation_slot=slot,
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    "That reservation time is already booked for this date."
                )
        return cleaned
