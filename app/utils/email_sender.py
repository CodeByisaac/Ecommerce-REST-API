import smtplib
from email.mime.text import MIMEText #create email messages in plain text format
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# get email configuration details securely from .env
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

#send an order confirmation mail to the specified recipient
def send_order_email(to_email: str, order_summary: str):
    message = MIMEMultipart()
    message["From"] = EMAIL_USER
    message["To"] = to_email
    message["Subject"] = "Your Order Confirmation"

    message.attach(MIMEText(order_summary, "plain"))

    try:
        #connection to the smtp server
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(message) #send the email
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)
