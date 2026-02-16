from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from students.models import Student
from .models import StudentApplication, GalleryItem, StudentLifeItem, LeadershipProfile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from students.utils import send_registration_email
from .forms import GalleryUploadForm, StudentLifeForm, LeadershipForm
# --------------------------
# STAFF LOGIN
# --------------------------
def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('staff:dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'staff/login.html')


# --------------------------
# STAFF CHECK
# --------------------------
def is_staff_user(user):
    """Allow only users in 'Staff' group or superusers."""
    return user.groups.filter(name='Staff').exists() or user.is_superuser


# --------------------------
# DASHBOARD
# --------------------------
@login_required
@user_passes_test(is_staff_user)
def dashboard(request):
    total_students = Student.objects.count()
    total_applications = StudentApplication.objects.count()
    pending_apps = StudentApplication.objects.filter(status='pending').count()
    approved_apps = StudentApplication.objects.filter(status='approved').count()
    rejected_apps = StudentApplication.objects.filter(status='rejected').count()

    context = {
        'total_students': total_students,
        'total_applications': total_applications,
        'pending_apps': pending_apps,
        'approved_apps': approved_apps,
        'rejected_apps': rejected_apps,
    }
    return render(request, 'staff/dashboard.html', context)


# --------------------------
# APPLICATIONS REVIEW
# --------------------------
@login_required
@user_passes_test(is_staff_user)
def applications_review(request):
    applications = StudentApplication.objects.all().order_by('-submitted_at')

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        action = request.POST.get('action')
        application = get_object_or_404(StudentApplication, id=app_id)

        if action == 'approve':
            application.status = 'approved'
            application.save()

            try:
                # ✅ Use your utility to send the correct registration email
                send_registration_email(application.email, application.registration_number)
                messages.success(
                    request,
                    f"{application.student_name}'s application was approved and an email was sent."
                )
            except Exception as e:
                messages.warning(
                    request,
                    f"Application approved but email could not be sent: {e}"
                )

        elif action == 'reject':
            application.status = 'rejected'
            application.save()
            messages.info(
                request,
                f"{application.student_name}'s application was rejected."
            )

        return redirect('staff:applications')

    return render(request, 'staff/applications.html', {'applications': applications})

# --------------------------
# ADMISSIONS REPORT
# --------------------------
@login_required
@user_passes_test(is_staff_user)
def admissions_report(request):
    summary = StudentApplication.objects.aggregate(
        total=Count('id'),
        approved=Count('id', filter=Q(status='approved')),
        rejected=Count('id', filter=Q(status='rejected')),
        pending=Count('id', filter=Q(status='pending')),
    )

    by_class = StudentApplication.objects.values('class_applied').annotate(
        total=Count('id')
    ).order_by('class_applied')

    return render(request, 'staff/reports.html', {
        'summary': summary,
        'by_class': by_class
    })


# --------------------------
# STAFF LOGOUT
# --------------------------
@login_required
def staff_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('staff:login')

@login_required
def upload_media(request):
    if request.method == 'POST':
        form = GalleryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Media uploaded successfully!')
            return redirect('staff:dashboard')
    else:
        form = GalleryUploadForm()

    return render(request, 'staff/upload_media.html', {'form': form})

@login_required
def delete_gallery_item(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)

    # Optional: Delete the actual file from storage to save space
    if item.image:
        item.image.delete()
    if item.video:
        item.video.delete()

    item.delete()
    messages.success(request, 'Item deleted successfully.')
    return redirect('public:gallery')

@login_required
def manage_student_life(request):
    if request.method == 'POST':
        form = StudentLifeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully!')
            return redirect('staff:manage_student_life')
    else:
        form = StudentLifeForm()

    # Get all items to show in a list
    items = StudentLifeItem.objects.all().order_by('-date_added')
    return render(request, 'staff/manage_student_life.html', {'form': form, 'items': items})

@login_required
def delete_student_life(request, pk):
    item = get_object_or_404(StudentLifeItem, pk=pk)
    item.delete()
    messages.success(request, 'Item deleted successfully.')
    return redirect('staff:manage_student_life')

@login_required
def manage_leadership(request):
    if request.method == 'POST':
        form = LeadershipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile added successfully!')
            return redirect('staff:manage_leadership')
    else:
        form = LeadershipForm()

    # Sort by 'order'
    staff_members = LeadershipProfile.objects.all().order_by('order')
    return render(request, 'staff/manage_leadership.html', {'form': form, 'staff_members': staff_members})

@login_required
def delete_leadership(request, pk):
    profile = get_object_or_404(LeadershipProfile, pk=pk)
    profile.delete()
    messages.success(request, 'Profile deleted.')
    return redirect('staff:manage_leadership')