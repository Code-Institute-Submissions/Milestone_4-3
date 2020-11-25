from django.conf import settings
from django.shortcuts import get_object_or_404
import datetime

from properties.models import Property

def booking_contents(request):

    booking_items = []
    total = 0
    booking_count = 0

    book_ses = request.session.get('book_ses', [])

    for i in range(len(book_ses)):
        one_book = book_ses[i]    
        property = get_object_or_404(Property, pk=one_book['property']) 
        delta = datetime.datetime.strptime(one_book['check_out'], '%Y-%m-%d') - datetime.datetime.strptime(one_book['check_in'], '%Y-%m-%d')
        # print(f"{delta} from {one_book['check_in']} to {one_book['check_out']}")
        price_day = property.daily_price
        total += (delta.days + 1) * price_day
        booking_count += 1

        booking_items.append({
             'property_id': one_book['property'],
             'days': delta.days + 1,
             'subtotal': (delta.days + 1) * price_day,
             'check_in': one_book['check_in'],
             'check_out': one_book['check_out'],
             'property': property,
         })

    context = {
        'booking_items': booking_items,
        'total': total,
        'booking_count': booking_count,
    }

    return context