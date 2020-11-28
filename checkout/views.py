from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    booking = request.session.get('book_ses', {})
    if not booking:
        messages.error(request, "You dont have any bookings yet")
        return redirect(reverse('listings'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)
