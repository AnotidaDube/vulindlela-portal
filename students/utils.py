from django.core.mail import send_mail
from django.conf import settings

def send_registration_email(email, reg_no):
    link = f"{settings.SITE_URL}/students/register/?reg_no={reg_no}"  # e.g. http://127.0.0.1:8000
    subject = "Application Received – Complete Your Registration"
    message = (
        f"Dear Applicant,\n\n"
        f"Thank you for applying. Your registration number is {reg_no}.\n\n"
        f"Once approved, you will be able to complete registration using this link:\n{link}\n\n"
        f"Regards,\nSchool Administration"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
