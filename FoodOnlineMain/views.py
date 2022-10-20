from django.shortcuts import render
from django.http import HttpResponse

#create your views here
def home(request):
    return render(request, 'home.html')
