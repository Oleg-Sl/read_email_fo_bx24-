from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import smtplib

import secrets


def send_mail(to_email, head, body, f_data, f_name):
    secret_data = secrets.get_secrets()
    if not secret_data or "server" not in secret_data or "username" not in secret_data or "password" not in secret_data:
        return None

    msg = MIMEMultipart()
    password = secret_data["password"]
    msg['From'] = secret_data["username"]
    msg['To'] = to_email
    msg['Subject'] = head
    if body:
        msg.attach(MIMEText(body))
    if f_data:
        attachment = MIMEBase('application', "octet-stream")
        attachment.set_payload(f_data)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{f_name}"')
        msg.attach(attachment)

    # Отправка сообщения
    server = smtplib.SMTP(f'{secret_data["server"]}: 25')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


