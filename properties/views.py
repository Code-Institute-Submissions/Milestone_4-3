from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Property
from .forms import PropertyForm, PropertyImagesForm
from booking.models import Booking
import datetime
from django.template.defaultfilters import register


from django.contrib.auth.decorators import login_required

# Create your views here.

def all_properties(request):
    """ A view to show all properies """

    properties = Property.objects.all()

    context = {
        'properties': properties,
    }

    return render(request, 'properties/properties.html', context)

@login_required
def listings(request):
    properties = Property.objects.all()

    context = {
        'properties': properties,
    }
    return render(request, 'properties/properties.html', context)


def property_details(request, property_id):
    """ A view to show property details """

    property = get_object_or_404(Property, pk=property_id)
    reserved_dates = []

    reserved_all = Booking.objects.filter(book_property=property, book_check_in__gte=datetime.date.today())
    for reserved in reserved_all:
        delta = reserved.book_check_out - reserved.book_check_in

        for i in range(delta.days + 1):
            format_date = (reserved.book_check_in + datetime.timedelta(days=i)).strftime("'%m/%d/%Y'")
            reserved_dates.append(format_date)
            # print(format_date)

    separator = ', '
    reserved = separator.join(reserved_dates)

    book_ses = request.session.get('book_ses', [])
    booked_dates=[]

    if any(d['property'] == property_id for d in book_ses):
        # for one_book in book_ses:
        for i in range(len(book_ses)):
            one_book = book_ses[i]    
            if(one_book['property'] == property_id):
                old_in = datetime.datetime.strptime(one_book['check_in'],'%Y-%m-%d')
                old_out = datetime.datetime.strptime(one_book['check_out'], '%Y-%m-%d')  
                delta_old = old_out-old_in  
                for i in range(delta_old.days + 1):
                    format_date = (old_in + datetime.timedelta(days=i)).strftime("'%Y-%m-%d'")
                    booked_dates.append(format_date)
                print('ok')

    booked = separator.join(booked_dates)

    context = {
        'property': property,
        'reserved': reserved,
        'booked': booked
    }

    return render(request, 'properties/property_details.html', context)

@login_required
def add_property(request):
    """ Add a property to rent """
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property added')
            return redirect(reverse('add_property'))
        else:
            messages.error(request, 'Property not added, please try again')
    else:
        form = PropertyForm()

    template = 'properties/add_property.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_property(request, property_id):
    """ Edit a property """
    property = get_object_or_404(Property, pk=property_id)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            property = form.save()
            messages.success(request, 'Property Successfully updated')
            return redirect(reverse('property_details', args=[property.id]))
        else:
            messages.error(request, 'Failed to update property.<br>Please ensure the form is valid.')
    else:
        form = PropertyForm(instance=property)

    template = 'properties/edit_property.html'
    context = { 
        'form': form,
        'property': property,
    }

    return render(request, template, context)

@login_required
def delete_property(request, property_id):
    """ Delete a property """
    property = get_object_or_404(Property, pk=property_id)
    property.delete()
    messages.success(request, 'Property removed')
    return redirect(reverse('properties'))

@login_required
def property_images(request, property_id):
    """ Change property additional images """
    template = 'properties/property_images.html'
    form = PropertyImagesForm(request.POST, request.FILES)

    context = { 
        'form': form,
        'property_id': property_id,
    }

    return render(request, template, context)
