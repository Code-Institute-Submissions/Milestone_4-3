from django.shortcuts import render

def index(request):
    """ view that returns the index page """
    return render(request, 'home/index.html')
