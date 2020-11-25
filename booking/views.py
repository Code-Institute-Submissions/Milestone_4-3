from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import datetime

from .models import Booking
from properties.models import Property

# Create your views here.

def view_booking(request):
    """ A view that renders current bookings"""

    return render(request, 'booking/booking.html')


def add_booking(request, property_id):

    p = int(property_id)
    redirect_url = request.POST.get('redirect_url')
    
    invalid_dates = False
    #get the property 
    book_ses = request.session.get('book_ses', [])

    guest_id = request.user

    # YYYY-MM-DD
    # datetime(
    # strftime("%Y-%m-%d")
    # datetime.datetime.strptime('10/05/2012', '%d/%m/%Y').strftime('%Y-%m-%d')

    check_in_date = request.POST.get('book_start')
    check_out_date = request.POST.get('book_end')

    check_in = datetime.datetime.strptime(check_in_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    check_out = datetime.datetime.strptime(check_out_date, '%m/%d/%Y').strftime('%Y-%m-%d')

    # check wether the dates are valid
    # case 1: a property is booked before the check_in date, and checks out after the requested check_in date
    case_1 = Booking.objects.filter(book_property=property_id, book_check_in__lte=check_in, book_check_out__gte=check_in).exists()

    # case 2: a property is booked before the requested check_out date and check_out date is after requested check_out date
    case_2 = Booking.objects.filter(book_property=property_id, book_check_in__lte=check_out, book_check_out__gte=check_out).exists()
    
    case_3 = Booking.objects.filter(book_property=property_id, book_check_in__gte=check_in, book_check_out__lte=check_out).exists()


    # if either of these is true, abort 
    if case_1 or case_2 or case_3:
        messages.error(request, 'This property is not available on your selected dates')           

    else:    
        # dates are valid -- will have to save once payment is done            
        # property = get_object_or_404(Property, pk=property_id)
        # booking = Booking(book_user = request.user, book_property = property, book_check_in = check_in,  book_check_out = check_out )
        # booking.save()

        if any(d['property'] == p for d in book_ses):
            # for one_book in book_ses:
            for i in range(len(book_ses)):
                one_book = book_ses[i]    
                if(one_book['property'] == p):
                    print("do date check")
                    old_in = datetime.datetime.strptime(one_book['check_in'],'%Y-%m-%d')
                    old_out = datetime.datetime.strptime(one_book['check_out'], '%Y-%m-%d')

                    middle = datetime.datetime.strptime(check_in_date, '%m/%d/%Y')
                    middle2 = datetime.datetime.strptime(check_out_date, '%m/%d/%Y')

                    if (old_in <= middle <= old_out) or (old_in <= middle2 <= old_out):
                        print("change in interval, update")
                        book_ses[i] = {'property': p, 'check_in': check_in, 'check_out': check_out}
                        break
                    else:
                        print("new interval, add")
                        book_ses.append({'property': p, 'check_in': check_in, 'check_out': check_out})
                    # print(f"sdsdsdso{old_in}{middle}{old_out}")

            # book_ses[property_id][1] = {'check_in': check_in, 'check_out': check_out}
        else:
            book_ses.append({'property': p, 'check_in': check_in, 'check_out': check_out})
            print('to add')

        request.session['book_ses'] = book_ses

    print(request.session['book_ses'])    
    return redirect(redirect_url)