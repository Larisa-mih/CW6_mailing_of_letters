import smtplib
from datetime import datetime, timedelta
import pytz
from django.core.mail import send_mail
from config import settings
from newsletter.models import Mail, LogAttempt


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mail.objects.filter(mail_datetime__lte=current_datetime,
                                   mail_status__in=[Mail.StatusOfMail.CREATED, Mail.StatusOfMail.LAUNCHED],
                                   mail_active=True)

    for mailing in mailings:
        try:
            send_mail(
                subject=mailing.message.message_title,
                message=mailing.message.message_content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.client.all()],
                fail_silently=False,
            )
            if mailing.mail_periodicity == Mail.PeriodicityOfMail.ONCE_DAY:
                mailing.mail_datetime_last = current_datetime + timedelta(days=1)
                mailing.mail_status = Mail.StatusOfMail.LAUNCHED
            elif mailing.mail_periodicity == Mail.PeriodicityOfMail.ONCE_WEEK:
                mailing.mail_datetime_last = current_datetime + timedelta(days=7)
                mailing.mail_status = Mail.StatusOfMail.LAUNCHED
            elif mailing.mail_periodicity == Mail.PeriodicityOfMail.ONCE_MONTH:
                mailing.mail_datetime_last = current_datetime + timedelta(days=30)
                mailing.mail_status = Mail.StatusOfMail.LAUNCHED
            mailing.save()

            status = LogAttempt.StatusOfLogAttempt.SUCCESS
            server_response = 'успешно'

        except smtplib.SMTPResponseException as e:
            status = LogAttempt.StatusOfLogAttempt.FAILED
            server_response = str(e)
        finally:
            LogAttempt.objects.create(
                mail_settings=mailing,
                attempt_status=status,
                server_response=server_response,
            )
