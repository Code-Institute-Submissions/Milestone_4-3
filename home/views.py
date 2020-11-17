from django.shortcuts import render
from django.contrib import messages
from properties.models import Property


def index(request):
    """ view that returns the index page """

    last_six = Property.objects.order_by('created')[:6]
    last_six_in_ascending_order = reversed(last_six)

    carousel_items = Property.objects.order_by('rating')[:5]

    context = {
        'properties': last_six_in_ascending_order,
        'carousel_items': carousel_items,
    }

    return render(request, 'home/index.html', context)
