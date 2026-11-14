from django.shortcuts import render

def app(request):
    return render(request, 'Django_app/app.html')
