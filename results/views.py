# results/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Mark, Term
from teachers.models import Student, Subject, Teacher
from django.urls import reverse
from django.db.models import Avg

def add_or_update_mark(request):
    """
    Endpoint for teacher POST to create/update a mark.
    Expects: registration_number (or student id), subject id, term id, score, comment (optional).
    After saving we redirect to the student's results page (so student view will show it).
    """
    if request.method != 'POST':
        return redirect('teacher_dashboard')

    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        messages.error(request, "Please login first.")
        return redirect('teacher_login')

    teacher = get_object_or_404(Teacher, id=teacher_id)

    # accept either student id or registration_number
    student_id = request.POST.get('student') or None
    reg_no = request.POST.get('registration_number') or None

    subject_id = request.POST.get('subject')
    term_id = request.POST.get('term')
    score = request.POST.get('score')
    comment = request.POST.get('comment', '')

    # find student
    student = None
    if student_id:
        student = get_object_or_404(Student, id=student_id)
    elif reg_no:
        student = Student.objects.filter(registration_number__iexact=reg_no).first()

    if not student or not subject_id or not term_id or score is None:
        messages.error(request, "Missing required fields.")
        return redirect('teacher_dashboard')

    subject = get_object_or_404(Subject, id=subject_id)
    term = get_object_or_404(Term, id=term_id)

    mark, created = Mark.objects.update_or_create(
        student=student,
        subject=subject,
        term=term,
        defaults={'score': score, 'comment': comment, 'teacher': teacher}
    )

    messages.success(request, f"Mark {'created' if created else 'updated'} for {student.full_name} - {subject.name}")
    # redirect to the student's results page, with term selected
    url = reverse('results:student_results') + f'?student={student.id}&term={term.id}'
    return redirect(url)

def student_results(request):
    # Allow viewing by logged-in student OR admin/teacher viewing a student's results by ?student=ID
    session_student_id = request.session.get('student_id')
    student_id = request.GET.get('student') or session_student_id

    if not student_id:
        messages.error(request, "Please login to view results.")
        return redirect('students:student_login')

    student = get_object_or_404(Student, id=student_id)

    term_id = request.GET.get('term')
    term = Term.objects.filter(id=term_id).first() if term_id else Term.objects.filter(is_active=True).first()

    marks = Mark.objects.filter(student=student, term=term).select_related('subject', 'teacher') if term else []

    # compute average
    average = None
    if marks:
        avg = marks.aggregate(avg_score=Avg('score'))['avg_score']
        if avg is not None:
            average = round(float(avg), 2)

    # compute class position if you want: average per student across same class and term
    position = None
    if term:
        class_students = Student.objects.filter(class_assigned=student.class_assigned)
        averages = []
        for s in class_students:
            s_avg = Mark.objects.filter(student=s, term=term).aggregate(avg_score=Avg('score'))['avg_score']
            if s_avg is not None:
                averages.append((s.id, float(s_avg)))
        averages.sort(key=lambda x: x[1], reverse=True)
        for idx, (sid, _) in enumerate(averages, start=1):
            if sid == student.id:
                position = idx
                break

    terms = Term.objects.all()
    return render(request, 'results/student_results.html', {
        'student': student,
        'term': term,
        'terms': terms,
        'marks': marks,
        'average': average,
        'position': position,
    })

# Create your views here.
