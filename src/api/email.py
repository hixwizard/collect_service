from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.template.loader import render_to_string

from .models import Collect, Payment


def get_email_connection():
    """Создание подключения к email серверу с настройками из settings."""
    return get_connection(
        backend=settings.EMAIL_BACKEND,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
        use_ssl=settings.EMAIL_USE_SSL,
        fail_silently=False,
    )


def send_collect_created_email(collect: Collect):
    """Отправка email автору о создании сбора."""
    subject = f'Создан новый сбор: {collect.title}'
    html_message = render_to_string('emails/collect_created.html', {
        'author_username': collect.author.username,
        'collect_title': collect.title,
        'description': collect.description,
        'reason': collect.get_reason_display(),
        'final_price': collect.final_price,
        'end_date': collect.end_date,
    })
    connection = get_email_connection()
    connection.open()
    try:
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[collect.author.email],
            connection=connection,
        )
        email.content_subtype = "html"
        email.send()
    finally:
        connection.close()


def send_payment_created_email(payment: Payment):
    """Отправка email автору сбора и донатеру о создании платежа."""
    collect = payment.collect
    donor = payment.user
    connection = get_email_connection()
    connection.open()
    try:
        subject = f'Новое пожертвование для сбора: {collect.title}'
        html_message = render_to_string('emails/to_author.html', {
            'author_username': collect.author.username,
            'donor_name': donor.username,
            'amount': payment.amount,
            'collect_title': collect.title,
            'payment_date': payment.created_at.strftime("%d.%m.%Y %H:%M"),
        })
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[collect.author.email],
            connection=connection,
        )
        email.content_subtype = "html"
        email.send()
        subject = f'Вы сделали пожертвование для сбора: {collect.title}'
        html_message = render_to_string('emails/to_donator.html', {
            'donor_username': donor.username,
            'amount': payment.amount,
            'collect_title': collect.title,
            'author_username': collect.author.username,
            'payment_date': payment.created_at.strftime("%d.%m.%Y %H:%M"),
        })
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[donor.email],
            connection=connection,
        )
        email.content_subtype = "html"
        email.send()
    finally:
        connection.close()
