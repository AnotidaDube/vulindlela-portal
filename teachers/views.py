from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Teacher
from django.shortcuts import get_object_or_404
from students.models import Student
from django.contrib.auth.hashers import make_password
from .models import Teacher, Subject, Class
from results.models import Term, Mark


def teacher_login(request):
    if request.method == 'POST':
        national_id = request.POST.get('national_id')
        password = request.POST.get('password')

        try:
            teacher = Teacher.objects.get(national_id=national_id)
            if teacher.check_password(password):
                request.session['teacher_id'] = teacher.id
                messages.success(request, f"Welcome {teacher.full_name}!")
                return redirect('teacher_dashboard')
            else:
                messages.error(request, 'Invalid password')
        except Teacher.DoesNotExist:
            messages.error(request, 'No teacher found with that National ID')

    return render(request, 'teachers/login.html')


def teacher_dashboard(request):
    # Ensure teacher is logged in
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        messages.error(request, "Please login first")
        return redirect('teacher_login')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    subjects = teacher.subjects.all()
    terms = Term.objects.all()

    search_reg = request.GET.get('registration_number')
    students = Student.objects.all()
    student = None  # ✅ Define early to avoid UnboundLocalError

    if search_reg:
        students = students.filter(registration_number__icontains=search_reg)
        try:
            student = Student.objects.get(registration_number=search_reg)
        except Student.DoesNotExist:
            messages.warning(request, "Student not found")
    else:
        students = []

    # Handle adding marks
    if request.method == 'POST':
        student_reg = request.POST.get('student_reg')
        subject_id = request.POST.get('subject_id')
        term_id = request.POST.get('term_id')
        score = request.POST.get('score')
        comment = request.POST.get('comment')

        if student_reg and subject_id and term_id and score:
            try:
                student = Student.objects.get(registration_number=student_reg)
                subject = Subject.objects.get(id=subject_id)
                term = Term.objects.get(id=term_id)

                Mark.objects.update_or_create(
                    student=student,
                    subject=subject,
                    term=term,
                    defaults={'score': score, 'comment': comment, 'teacher': teacher}
                )
                messages.success(request, f"Mark recorded for {student.first_name + ' ' + student.last_name}")

                search_reg = student.registration_number
                students = Student.objects.filter(registration_number__icontains=search_reg)

            except Student.DoesNotExist:
                messages.error(request, "No student found with that registration number")
            except Subject.DoesNotExist:
                messages.error(request, "Selected subject not found")
            except Term.DoesNotExist:
                messages.error(request, "Selected term not found")

    # ✅ Safe mark retrieval
    marks_records = Mark.objects.filter(student=student) if student else []

    return render(request, 'teachers/dashboard.html', {
        'teacher': teacher,
        'subjects': subjects,
        'terms': terms,
        'students': students,
        'search_reg': search_reg,
        'marks_records': marks_records,
    })

def teacher_logout(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('teacher_login')


def add_marks(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        messages.error(request, "Please log in first.")
        return redirect('teacher_login')

    teacher = Teacher.objects.get(id=teacher_id)
    subjects = teacher.subjects.all()
    students = Student.objects.all()  # optionally filter by class

    if request.method == 'POST':
        reg_number = request.POST.get('student_reg')
        try:
            student = Student.objects.get(registration_number=reg_number)
        except Student.DoesNotExist:
            messages.error(request, 'No student found with that registration number')
            return redirect('teacher_dashboard')
    
        subject_id = request.POST.get('subject')
        score = request.POST.get('score')
        subject = Subject.objects.get(id=subject_id)

        Mark.objects.create(student=student, subject=subject, score=score)
        messages.success(request, f"Mark recorded for {student.full_name}")
        return redirect('teacher_dashboard')
    return render(request, 'teachers/add_marks.html', {'subjects': subjects, 'students': students})


def teacher_signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        national_id = request.POST.get('national_id')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if National ID already exists
        if Teacher.objects.filter(national_id=national_id).exists():
            messages.error(request, 'A teacher with this National ID already exists.')
            return redirect('teacher_signup')

        # Create teacher account with hashed password
        teacher = Teacher.objects.create(
            full_name=full_name,
            national_id=national_id,
            email=email,
            password=make_password(password)
        )

        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('teacher_login')

    return render(request, 'teachers/signup.html')


# Create your views here.
