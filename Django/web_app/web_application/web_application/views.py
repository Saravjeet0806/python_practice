from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'website/index.html')

def about(request):
    return HttpResponse("hello, I am at About Page")

def contact(request):
    return HttpResponse("Meow, I am at Contacts Page")
