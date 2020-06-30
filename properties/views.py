from django.shortcuts import render, get_object_or_404
from .models import Property
from .forms import PropertyForm

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

def add_property(request):
    """ Add a property to rent """
    form = PropertyForm()
    template = 'properties/add_property.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
