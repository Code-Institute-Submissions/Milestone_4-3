from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Property
from .forms import PropertyForm

from django.contrib.auth.decorators import login_required

# Create your views here.

def all_properties(request):
    """ A view to show all properies """

    properties = Property.objects.all()

    context = {
        'properties': properties,
    }

    return render(request, 'properties/properties.html', context)

def property_details(request, property_id):
    """ A view to show property details """

    property = get_object_or_404(Property, pk=property_id)

    context = {
        'property': property,
    }

    return render(request, 'properties/property_details.html', context)

@login_required
def add_property(request):
    """ Add a property to rent """
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('add_property'))
        # else:
            # error
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
    return redirect(reverse('properties'))
