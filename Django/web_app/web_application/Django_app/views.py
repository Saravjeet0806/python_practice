from django.shortcuts import render
from .models import ChaiVarity

def app(request):
    chais = ChaiVarity.objects.all

    return render(request, 'Django_app/app.html', {'chais': chais})
