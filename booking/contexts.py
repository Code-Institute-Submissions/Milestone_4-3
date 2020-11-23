from django.conf import settings

def booking_contents(request):

    booking_items = []
    total = 0
    booking_count = 0

    context = {
        'booking_items': booking_items,
        'total': total,
        'booking_count': booking_count,
    }

    return context