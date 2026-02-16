from django.shortcuts import render
from .models import SchoolUpdate


def welcome(request):
    updates = SchoolUpdate.objects.order_by('-posted_on')[:6]  # latest 6 updates
    return render(request, 'coreapp/welcome.html', {'updates': updates})


# Create your views here.
