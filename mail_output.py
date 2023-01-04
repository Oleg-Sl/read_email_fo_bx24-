from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import smtplib
import os


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
        # attachment.set_payload(f_data)
        # msg.set_payload(f_data)
        # msg['Content-Transfer-Encoding'] = 'base64'
        attachment.add_header('Content-Disposition', f'attachment; filename="{f_name}"')
        msg.attach(attachment)

    # Отправка сообщения
    server = smtplib.SMTP(f'{secret_data["server"]}: 25')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()




# def send_mail(to_email, head, body, file):
#     secret_data = secrets.get_secrets()
#     if not secret_data or "server" not in secret_data or "username" not in secret_data or "password" not in secret_data:
#         return None
#
#     msg = MIMEMultipart()
#
#     password = secret_data["server"]
#     msg['From'] = secret_data["username"]
#     msg['To'] = to_email
#     # Заголовок
#     msg['Subject'] = head
#     # Тело запроса
#     if body:
#         msg.attach(MIMEText(body))
#
#     attachment = MIMEBase('application', "octet-stream")
#     try:
#         file = "C3_SimpleBashUtils-0.zip"
#         with open(f"/home/oleg/Desktop/files/{file}", "rb") as fh:
#             data = fh.read()
#         attachment.set_payload(data)
#         encoders.encode_base64(attachment)
#         attachment.add_header('Content-Disposition', f'attachment; filename="{file}"')
#         msg.attach(attachment)
#     except IOError:
#         msg = "Error opening attachment file %s" % file
#         print(msg)
#         # sys.exit(1)
#
#     # msg.attach(MIMEImage(file("google.jpg").read()))
#
#     server = smtplib.SMTP(f'{secret_data["server"]}: 25')
#     server.starttls()
#     server.login(msg['From'], password)
#     server.sendmail(msg['From'], msg['To'], msg.as_string())
#     server.quit()
#     print("successfully sent email to %s:" % (msg['To']))
#
# msg['To'] = "slepcov_oleg@mail.ru"
# msg['To'] = "djmovi@mail.ru"

