from django.http import HttpResponse

from .models import Order, OrderLineItem
from properties.models import Property
from profiles.models import UserProfile
from django.db import models
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

import json
import time
import datetime

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )        

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        booking = intent.metadata.booking
        save_info = intent.metadata.save_info

        # CHECK HEREEEEE
        billing_details = intent.charges.data[0].billing_details
        total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the billing details
        for field, value in billing_details.address.items():
            if value == "":
                billing_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)

            class Types(models.TextChoices):
                OWNER = "OWNER", "Owner"
                TENANT = "TENANT", "Tenant"

            base_type = Types.TENANT
            if save_info:
                profile.default_phone_number = billing_details.phone
                profile.default_country = billing_details.address.country
                profile.default_postcode = billing_details.address.postal_code
                profile.default_town_or_city = billing_details.address.city
                profile.default_street_address1 = billing_details.address.line1
                profile.default_street_address2 = billing_details.address.line2
                profile.default_county = billing_details.address.state
                profile.default_type = base_type
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=billing_details.name,
                    user_profile=profile,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    country__iexact=billing_details.address.country,
                    postcode__iexact=billing_details.address.postal_code,
                    town_or_city__iexact=billing_details.address.city,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    county__iexact=billing_details.address.state,
                    total=total,
                    original_book=booking,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=billing_details.name,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    country=billing_details.address.country,
                    postcode=billing_details.address.postal_code,
                    town_or_city=billing_details.address.city,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    county=billing_details.address.state,
                    original_booking=booking,
                    stripe_pid=pid,
                )
                for i in range(len(json.loads(booking))):
                    one_book = json.loads(booking)[i]
                    delta = datetime.datetime.strptime(one_book['check_out'], '%Y-%m-%d') - datetime.datetime.strptime(one_book['check_in'], '%Y-%m-%d')
                    days = delta.days + 1

                    property = Property.objects.get(id=one_book['property'])
                    order_line_item = OrderLineItem(
                        order=order,
                        property=property,
                        check_in=one_book['check_in'],
                        check_out=one_book['check_out'],
                        days=days,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200)

