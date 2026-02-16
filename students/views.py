from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from .utils import send_registration_email
from django.views.decorators.csrf import csrf_exempt

from .models import Student
from .forms import ForgotPasswordForm, ResetPasswordForm
from students.models import Class
from staff.models import StudentApplication


# Custom token generator for students
class StudentTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, student, timestamp):
        return f"{student.pk}{timestamp}{student.email}"


student_token_generator = StudentTokenGenerator()


# ===============================
# Student Application (Apply First)
# ===============================
def student_apply(request):
    if request.method == 'POST':
        name = request.POST.get('student_name')
        email = request.POST.get('email')
        applied_class_id = request.POST.get('applied_class')
        prev_grade_level = request.POST.get('previous_grade_level')
        prev_grade_results = request.POST.get('previous_grade_results')

        # ✅ Validate required fields
        if not all([name, email, applied_class_id, prev_grade_level, prev_grade_results]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('students:apply')

        # ✅ Generate registration number safely
        last_app = StudentApplication.objects.order_by('id').last()
        new_id = (last_app.id + 1) if last_app else 1
        reg_no = f"VSS2025-{new_id:04d}"

        # ✅ Get selected class
        applied_class = Class.objects.get(id=applied_class_id)

        # ✅ Create and save the application
        student_app = StudentApplication.objects.create(
            student_name=name,
            email=email,
            registration_number=reg_no,
            applied_class=applied_class,
            previous_grade_level=prev_grade_level,
            previous_grade_results=prev_grade_results,
            status='pending'
        )

        messages.success(request, "Your application has been submitted successfully! Please wait for approval.")
        return redirect('students:application_success', reg_no=reg_no)

    # -----------------
    # GET request
    # -----------------
    classes = Class.objects.all().order_by('name')  # show in nice order
    return render(request, 'students/apply.html', {'classes': classes})

def application_success(request, reg_no: str):
    """Displays application submission success message."""
    return render(request, 'students/success.html', {'reg_no': reg_no})


# ===============================
# Student Registration (After Approval)
# ===============================
def student_register(request):
    reg_no = request.GET.get('reg_no') or request.POST.get('reg_no')
    application = get_object_or_404(StudentApplication, registration_number=reg_no)

    # Block if already registered
    if getattr(application, 'is_registered', False):
        messages.warning(request, "You have already completed registration.")
        return redirect('students:student_login')

    if request.method == "POST":
        email = request.POST.get('email')
        if Student.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect(f"{request.path}?reg_no={reg_no}")

        try:
            Student.objects.create(
                registration_number=application.registration_number,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=email,
                password=make_password(request.POST.get('password')),
                date_of_birth=request.POST.get('date_of_birth'),
                phone_number=request.POST.get('phone_number'),
                photo=request.FILES.get('photo') or None
            )

            # Mark application as registered
            application.is_registered = True
            application.save()

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('students:student_login')

        except IntegrityError:
            messages.error(request, "Registration failed due to duplicate or invalid data.")
            return redirect(f"{request.path}?reg_no={reg_no}")

    return render(request, "students/register.html", {
        "application": application,
        "reg_no": application.registration_number
        })

# ===============================
# Student Login / Dashboard / Logout
# ===============================
def student_login(request):
    if request.method == "POST":
        reg_no = request.POST.get("reg_no", "").strip()
        password = request.POST.get("password", "")

        try:
            student = Student.objects.get(registration_number=reg_no)
        except Student.DoesNotExist:
            messages.error(request, "Student not found")
            return redirect("students:student_login")

        # Determine if stored password is hashed
        if student.password.startswith('pbkdf2_') or student.password.startswith('argon2$'):
            # hashed password
            if check_password(password, student.password):
                request.session['student_id'] = student.id
                return redirect("students:dashboard")
            else:
                messages.error(request, "Incorrect password")
                return redirect("students:student_login")
        else:
            # plain password
            if password == student.password:
                # Optionally hash plain password after successful login
                student.password = make_password(password)
                student.save()
                request.session['student_id'] = student.id
                return redirect("students:dashboard")
            else:
                messages.error(request, "Incorrect password")
                return redirect("students:student_login")

    return render(request, "students/login.html")



def dashboard(request):
    """Displays student dashboard."""
    student_id = request.session.get('student_id')
    if not student_id:
        messages.error(request, "Please log in to access your dashboard.")
        return redirect('students:login')

    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students/dashboard.html', {'student': student})


def student_logout(request):
    """Logs out the student."""
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('students:student_login')


# ===============================
# Password Reset
# ===============================
def forgot_password(request):
    """Handles password reset request."""
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            reg_no = form.cleaned_data['registration_number']
            email = form.cleaned_data['email']

            try:
                student = Student.objects.get(registration_number=reg_no, email=email)
                uid = urlsafe_base64_encode(force_bytes(student.pk))
                token = student_token_generator.make_token(student)
                reset_link = request.build_absolute_uri(f"/students/reset-password/{uid}/{token}/")

                # Send reset email
                send_mail(
                    subject="Password Reset Request",
                    message=(
                        f"Dear {student.first_name},\n\n"
                        "You requested to reset your password.\n"
                        f"Click the link below to set a new password:\n{reset_link}\n\n"
                        "If you didn’t request this, please ignore this email."
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[student.email],
                    fail_silently=False,
                )

                messages.success(request, "Password reset link sent to your email.")
                return redirect('students:forgot_password')

            except Student.DoesNotExist:
                messages.error(request, "No matching record found.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'students/forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    """Handles actual password reset using token."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        student = Student.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Student.DoesNotExist):
        student = None

    if student and default_token_generator.check_token(student, token):
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                student.set_password(new_password)
                student.save()
                messages.success(request, "Password has been reset successfully.")
                return redirect('students:login')
        else:
            form = ResetPasswordForm()
        return render(request, 'students/reset_password.html', {'form': form})
    messages.error(request, "Invalid or expired link.")
    return redirect('students:forgot_password')


def view_subjects(request):
    return render(request, 'students/subjects.html')

def view_calendar(request):
    return render(request, 'students/calendar.html')

def view_timetable(request):
    return render(request, 'students/timetable.html')
def view_profile(request):
    registration_number = request.session.get('student_id')
    if not student_id:
        messages.error(request, "Please log in to access your profile.")
        return redirect('students:login')

    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students/profile.html', {'student': student})