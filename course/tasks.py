from django.core.mail import send_mail
from django.utils import timezone
from celery import shared_task
from config.settings import EMAIL_HOST_USER
from course.models import Subscription
from users.models import User


@shared_task
def sending_update_course(course):
    course_updates = Subscription.objects.filter(course=course.id)
    for update in course_updates:
        send_mail(
            subject='Course updated',
            message=f'Your course was updated - {update.course.title}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[update.user.email]
        )
    print("E-mail sent")


@shared_task()
def check_last_login():
    users = User.objects.filter(is_active=True)
    for user in users:
        if user.last_login is None:
            user.is_active = False
            user.save()
        elif timezone.now() - user.last_login > timezone.timedelta(days=30):
            user.is_active = False
            user.save()
