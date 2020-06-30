from django.shortcuts import render, get_object_or_404, redirect, reverse
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
