from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from staff.models import GalleryItem, StudentLifeItem, LeadershipProfile

def about_us(request):
    return render(request, 'public/about_us.html')

def vacancies(request):
    return render(request, 'public/vacancies.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Contact Message from {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(subject, full_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, f'Error sending message: {e}')

    return render(request, 'public/contact_us.html')

def gallery_view(request):
    photos = GalleryItem.objects.all().order_by('-date_added')
    return render(request, 'coreapp/gallery.html', {'photos': photos})

def academics(request):
    return render(request, 'public/academics.html')

def admissions(request):
    return render(request, 'public/admissions.html')

def student_life(request):
    # Separate the items by category so we can show them in different sections
    sports = StudentLifeItem.objects.filter(category='sport')
    clubs = StudentLifeItem.objects.filter(category='club')
    boarding = StudentLifeItem.objects.filter(category='boarding')

    context = {
        'sports': sports,
        'clubs': clubs,
        'boarding': boarding
    }
    return render(request, 'public/student_life.html', context)

def leadership(request):
    admins = LeadershipProfile.objects.filter(category='admin').order_by('order')
    teachers = LeadershipProfile.objects.filter(category='teacher').order_by('order')
    prefects = LeadershipProfile.objects.filter(category='prefect').order_by('order')

    return render(request, 'public/leadership.html', {
        'admins': admins,
        'teachers': teachers,
        'prefects': prefects
    })