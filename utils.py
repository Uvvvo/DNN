import logging
import smtplib

# إعداد نظام التسجيل
logging.basicConfig(filename='system_logs.log', level=logging.INFO)

def log_prediction(prediction):
    """
    تسجيل التنبؤات في ملف.
    """
    logging.info(f"Prediction: {prediction}")

def send_email(subject, message):
    """
    إرسال بريد إلكتروني.
    """
    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    password = "your_password"

    email_text = f"Subject: {subject}\n\n{message}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_text)