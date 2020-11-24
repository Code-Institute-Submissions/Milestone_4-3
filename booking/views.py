from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking

# Create your views here.

def view_booking(request):
    """ A view that renders current bookings"""

    return render(request, 'booking/booking.html')


def add_booking(request, property_id):

    redirect_url = request.POST.get('redirect_url')
    
    invalid_dates = False
    #get the property 
    property = property.objects.get(pk=property_id)
    guest_id = request.user
    check_in = request.session['start'] 
    check_out = request.session['end']

    # check wether the dates are valid
    # case 1: a property is booked before the check_in date, and checks out after the requested check_in date
    case_1 = Booking.objects.filter(property=property, check_in__lte=check_in, check_out__gte=check_in).exists()

    # case 2: a property is booked before the requested check_out date and check_out date is after requested check_out date
    case_2 = Booking.objects.filter(property=property, check_in__lte=check_out, check_out__gte=check_out).exists()
    
    case_3 = Booking.objects.filter(property=property, check_in__gte=check_in, check_out__lte=check_out).exists()


    # if either of these is true, abort 
    if case_1 or case_2 or case_3:
        messages.error(request, 'This property is not available on your selected dates')           

    else:    
        # dates are valid             
        booking = Booking(
            book_user = guest_id.id,
            book_property = property.id,
            book_check_in = check_in,
            book_check_out = check_out,
        )

    request.session['booking'] = booking
    return redirect(redirect_url)