from django.shortcuts import render
from django.http import HttpResponse


# def home(request):
#     return HttpResponse('Home')

def home(request):
    return render(request, 'web/home.html', {})
