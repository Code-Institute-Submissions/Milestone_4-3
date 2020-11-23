from django.shortcuts import render

# Create your views here.

def view_booking(request):
    """ A view that renders current bookings"""

    return render(request, 'booking/booking.html')
