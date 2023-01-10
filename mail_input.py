import poplib
import email
from email.header import decode_header
import base64
import re
from pprint import pprint
import bitrix as bx24
import secrets
import datetime
from html.parser import HTMLParser

PATTERN_DATE = "%Y-%m-%dT%H:%M:%S%z"


class MyHTMLParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.content = []

    def get_data(self):
        return self.content

    def handle_data(self, data):
        if not self.get_starttag_text() == "<style>" and data:
            self.content.append(data)


def byte_decode(raw, encoding="utf-8"):
    data = raw
    try:
        if isinstance(raw, bytes):
            data = raw.decode(encoding=encoding)
    except UnicodeDecodeError:
        if encoding != "cp1251":
            return byte_decode(raw, encoding="cp1251")

    return data


def get_id_deal_from_head(head):
    print(head)
    id_deal = None
    id_deal_regular = None
    if head:
        id_deal_regular = re.search("ID: (\d*);", head)
    if id_deal_regular and id_deal_regular.groups():
        id_deal = id_deal_regular.group(1)
    return id_deal


def create_deal(head, emailaddr, body, files):
    # Получение ID контакта по email
    contact = None
    contacts = bx24.get_contact_by_email(emailaddr)
    if contacts:
        contact = contacts[0]
    if body:
        parser = MyHTMLParser()
        parser.reset()
        parser.feed(body)
        body = " ".join(parser.get_data())

    fields = {
        "UF_CRM_1670388481": head,                                          # тема
        "UF_CRM_1670388688": body,                                          # тело письма
        "UF_CRM_1671445904": get_id_deal_from_head(head),                   # ID сделки, если будет в теме письма
        "UF_CRM_1671515915": emailaddr,                                     # email
        "UF_CRM_1671516029": contact.get("ID", None) if contact else None,  # ид контакта, если найдется
        "UF_CRM_1671611551": [{"fileData": list(file)} for file in files]   # вложения из почты
    }
    # pprint(fields["UF_CRM_1670388481"])
    # pprint(fields["UF_CRM_1671445904"])
    result = bx24.add_deal(fields)
    pprint({
        "date": str(datetime.datetime.now()),
        "result": result
    })


def get_head(msg):
    title = ""
    heads = decode_header(msg["Subject"]) if msg.get("Subject") else []
    for head, coding in heads:
        # print(head, " - ", coding)
        if head and coding:
            title += head.decode(coding)
        elif head:
            title += byte_decode(head)
    # head, coding = decode_header(msg["Subject"])[0] if msg.get("Subject") else (None, None)
    # head_1, coding_2 = decode_header(msg["Subject"])[0] if msg.get("Subject") else (None, None)
    # print(decode_header(msg["Subject"]))
    # if head and coding:
    #     head = head.decode(coding)
    # elif head:
    #     head = byte_decode(head)

    return title


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

        if f_name  and (disposition == "attachment" or maintype == "image"):
            regular = re.search(r"\?(.*)\?.*\?(.*)\?", f_name)
            if regular and regular.groups() and len(regular.groups()) == 2:
                data.append((byte_decode(base64.b64decode(regular.group(2)), regular.group(1)), f_data))
            else:
                data.append((f_name, f_data))

    return data


def get_body(msg):
    body = None
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype in ['text/plain', 'text/html'] and 'attachment' not in cdispo:
                charset = part.get_content_charset()
                body = part.get_payload(decode=True)
                if charset and isinstance(body, bytes):
                    body = body.decode(encoding=charset, errors="ignore")
                break
    else:
        charset = msg.get_content_charset()
        body = msg.get_payload(decode=True).decode(msg.get_content_charset())
        if charset and isinstance(body, bytes):
            body = body.decode(encoding=charset, errors="ignore")

    if isinstance(body, bytes):
        body = byte_decode(body)

    return body

    # data = None
    # for part in msg.walk():
    #     # print(part)
    #     maintype = part.get_content_maintype()
    #     subtype = part.get_content_subtype()
    #     charset = part.get_content_charset() or "utf-8"
    #     disposition = part.get_content_disposition()
    #     f_data = part.get_payload(decode=True)
    #     f_name = part.get_filename()
    #     is_multipart = msg.is_multipart()
    #     if maintype == "text":
    #         print("*"*88)
    #         print("is_multipart = ", is_multipart)
    #         print("maintype = ", maintype)
    #         print("subtype = ", subtype)
    #         print("disposition = ", disposition)
    #         print("charset = ", charset)
    #         print("f_name = ", f_name)
    #         print("f_data = ", f_data)
    #     if maintype == "text" and subtype == "plain" and disposition != "attachment" and charset == "us-ascii":
    #         data = f_data
    #     elif maintype == "text" and subtype == "plain" and disposition != "attachment":
    #         try:
    #             print("data = ", f_data.decode(encoding=charset, errors="ignore"))
    #             # print("data = ", base64.b64decode(f_data))
    #             # data = base64.b64decode(part.get_payload()).decode(encoding=charset, errors="ignore")
    #             # print("data = ", data)
    #         except ValueError as err:
    #             data = f_data
    #
    #     # elif maintype == "text" and subtype == "html" and disposition != "attachment":
    #     #     try:
    #     #         data = base64.b64decode(f_data)
    #     #     except Exception:
    #     #         data = f_data
    #
    # return data


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
    # handler_email(pop3server, 1649)
    # handler_email(pop3server, 1555)
    for i in range(secret_data["countmail"] + 1, mailcount + 1):
        print("Number mail: ", i)
        secrets.save_mailcount(i)
        handler_email(pop3server, i)

    pop3server.quit()


