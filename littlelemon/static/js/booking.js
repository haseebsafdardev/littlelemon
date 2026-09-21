document.addEventListener("DOMContentLoaded", () => {
    const dateInput = document.getElementById("id_reservation_date");
    const slotSelect = document.getElementById("id_reservation_slot");
    const results = document.getElementById("booking-results");
    const title = document.getElementById("bookings-title");

    if (!dateInput || !slotSelect) return;

    const today = new Date();
    const localToday = new Date(today.getTime() - today.getTimezoneOffset() * 60000)
        .toISOString()
        .slice(0, 10);

    if (!dateInput.value) {
        dateInput.value = localToday;
    }

    dateInput.min = localToday;

    function formatSlot(hour) {
        const h = Number(hour);
        const suffix = h >= 12 ? "PM" : "AM";
        const display = h % 12 || 12;
        return `${display} ${suffix}`;
    }

    function renderBookings(bookings, selectedDate) {
        title.textContent = `Bookings For ${selectedDate}`;

        const bookedSlots = new Set(
            bookings.map((booking) => Number(booking.fields.reservation_slot))
        );

        Array.from(slotSelect.options).forEach((option) => {
            if (!option.value) return;
            const isBooked = bookedSlots.has(Number(option.value));
            option.disabled = isBooked;
            option.textContent = `${formatSlot(option.value)}${isBooked ? " (Booked)" : ""}`;
        });

        if (bookings.length === 0) {
            results.innerHTML = '<p class="no-booking">No Bookings</p>';
            return;
        }

        results.innerHTML = bookings.map((booking) => {
            const name = booking.fields.first_name;
            const slot = formatSlot(booking.fields.reservation_slot);
            return `<p class="booking-item">${name} - ${slot}</p>`;
        }).join("");
    }

    async function loadBookings() {
        const selectedDate = dateInput.value;

        if (!selectedDate) {
            results.innerHTML = "<p>Select a reservation date.</p>";
            return;
        }

        results.innerHTML = "<p>Loading bookings...</p>";

        try {
            const response = await fetch(`/bookings?date=${encodeURIComponent(selectedDate)}`, {
                headers: { "Accept": "application/json" }
            });

            if (!response.ok) {
                throw new Error("Unable to load bookings.");
            }

            const bookings = await response.json();
            renderBookings(bookings, selectedDate);
        } catch (error) {
            results.innerHTML = `<p class="error">${error.message}</p>`;
        }
    }

    dateInput.addEventListener("change", loadBookings);
    loadBookings();
});
