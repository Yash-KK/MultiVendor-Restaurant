from django.shortcuts import HttpResponse, render

# Create your views here.
def v_profile(request):    
    return render(request, 'vendor/v_profile.html')

