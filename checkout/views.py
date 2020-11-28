from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from properties.models import Property
from booking.contexts import booking_contents

from .forms import OrderForm
from .models import Order, OrderLineItem
import stripe
import datetime

def checkout(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        booking = request.session.get('book_ses', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save()
            for i in range(len(booking)):
                try:
                    one_book = booking[i]
                    delta = datetime.datetime.strptime(one_book['check_out'], '%Y-%m-%d') - datetime.datetime.strptime(one_book['check_in'], '%Y-%m-%d')
                    days = delta.days + 1
                    property_line = get_object_or_404(Property, pk=one_book['property'])
                    order_line_item = OrderLineItem(
                        order=order,
                        property=property_line,
                        check_in=one_book['check_in'],
                        check_out=one_book['check_out'],
                        days=days,
                    )
                    order_line_item.save()
                    
                except Property.DoesNotExist:
                    messages.error(request, (
                        "One of the properties not found")
                    )
                    order.delete()
                    return redirect(reverse('view_booking'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        booking = request.session.get('book_ses', {})
        if not booking:
            messages.error(request, "You dont have any bookings yet")
            return redirect(reverse('listings'))

        current_book = booking_contents(request)
        total = current_book['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    """ Handle successful checkouts """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'book_ses' in request.session:
        del request.session['book_ses']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
