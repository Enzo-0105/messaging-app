# celery_tasks.py

from celery import Celery
from app import app

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

@celery.task
def send_email_task(recipient):
    import smtplib
    sender_email = "salakolateef331@gmail.com"
    SENDER_PASSWORD = "CPYEKYK2369hx22zvl"

    message = f"Subject: Test Email\n\nThis is a test email to {recipient}"

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message)

