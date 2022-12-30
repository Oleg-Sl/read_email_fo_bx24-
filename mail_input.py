import poplib
import email
from email.header import decode_header
import base64
import re
from pprint import pprint
import bitrix as bx24
import secrets


PATTERN_DATE = "%Y-%m-%dT%H:%M:%S%z"


def create_deal(head, emailaddr, body, files):
    # Получение ID контакта по email
    contact = None
    contacts = bx24.get_contact_by_email(emailaddr)
    if contacts:
        contact = contacts[0]
    fields = {
        "UF_CRM_1670388481": head,                                          # тема
        "UF_CRM_1670388688": str(body),                                     # тело письма
        "UF_CRM_1671445904": "",                                            # ид сделки, если будет в теме письма
        "UF_CRM_1671515915": emailaddr,                                     # email
        "UF_CRM_1671516029": contact.get("ID", None) if contact else None,  # ид контакта, если найдется
        "UF_CRM_1671611551": [{"fileData": file} for file in files]         # вложения из почты
    }
    pprint(fields)
    result = bx24.add_deal(fields)
    pprint(result)

def get_head(msg):
    head, coding = decode_header(msg["Subject"])[0]
    if head and coding:
        head = head.decode(coding)
    return head


def get_date(msg):
    letter_date = email.utils.parsedate_tz(msg["Date"])
    return letter_date


def get_email(msg):
    email_str = email.header.make_header(email.header.decode_header(msg['From']))
    res = re.search(r".*<(\S*)>", email_str.encode())
    addr = msg['From']
    if res and res.groups():
        addr = res.group(1)

    return addr


def get_files(msg):
    data = []
    for part in msg.walk():
        maintype = part.get_content_maintype()
        subtype = part.get_content_subtype()
        charset = part.get_content_charset()
        disposition = part.get_content_disposition()
        f_name = part.get_filename()
        f_data = part.get_payload()

        if f_name and f_data and disposition == "attachment":
            fname = re.search(r"\?.*\?.*\?(.*)\?", f_name)
            if fname and fname.groups():
                data.append((base64.b64decode(fname.group(1)).decode(), f_data))
            else:
                data.append((f_name, f_data))

    return data


def get_body(msg):
    data = None
    for part in msg.walk():
        maintype = part.get_content_maintype()
        subtype = part.get_content_subtype()
        charset = part.get_content_charset()
        disposition = part.get_content_disposition()
        f_data = part.get_payload()
        f_name = part.get_filename()

        if maintype == "text" and subtype == "plain" and disposition != "attachment" and charset == "us-ascii":
            data = f_data
        elif maintype == "text" and subtype == "plain" and disposition != "attachment":
            try:
                data = base64.b64decode(part.get_payload()).decode(encoding=charset, errors="ignore")
            except ValueError as err:
                data = f_data

    return data


def handler_email(pop3server, number):
    msg = email.message_from_bytes(b'\r\n'.join(pop3server.retr(number)[1]))
    head = get_head(msg)
    emailaddr = get_email(msg)
    body = get_body(msg)
    files = get_files(msg)
    create_deal(head=head, emailaddr=emailaddr, body=body, files=files)


def mail_get(**secret_data):
    pop3server = secret_data["server"]
    username = secret_data["username"]
    password = secret_data["password"]
    pop3server = poplib.POP3_SSL(pop3server)
    pop3server.getwelcome()
    pop3server.user(username)
    pop3server.pass_(password)
    pop3info = pop3server.stat()
    mailcount = pop3info[0]
    for i in range(secret_data["countmail"] + 1, mailcount + 1):
        handler_email(pop3server, i)

    secrets.save_mailcount(mailcount)
    pop3server.quit()
