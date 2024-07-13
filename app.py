# app.py

from flask import Flask, request, Response
from celery import Celery
import logging
from datetime import datetime

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Configure logging
log_file_path = '/var/log/messaging_system.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO)

@celery.task
def send_email_task(recipient):
    import smtplib
    sender_email = "salakolateef331@gmail.com"
    sender_password = "cunmvyjeomhxmzvl"

    message = f"Subject: Test Email\n\nThis is a test email to {recipient}"

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        send_email_task.delay(sendmail)
        return f"Email queued to {sendmail}"
    
    if talktome:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"talktome requested at {current_time}")
        return "Logged the current time"
    
    return "Use ?sendmail=email@example.com or ?talktome=yes"

@app.route('/logs')
def logs():
    def generate():
        with open(log_file_path) as f:
            for line in f:
                yield line
    return Response(generate(), mimetype='text/plain')
if __name__ == '__main__':
    app.run(debug=True)

