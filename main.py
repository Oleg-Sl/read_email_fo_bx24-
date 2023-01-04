#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
from mail_input import mail_get
from mail_output import send_mail
import secrets


def main():
    secret = secrets.get_secrets()
    if secret and "server" in secret and "username" in secret and "password" in secret and "countmail" in secret:
        mail_get(**secret)
    else:
        print("Отсутствует файл 'secrets.json' или данные в нем!")


# def send():
#     secret = secrets.get_secrets()

# 3764 - нет тела  сообщения
if __name__ == "__main__":
    # with open("/home/oleg/Desktop/files/Cate.jpg", "rb") as f:
    #     raw = f.read()
    # # data = raw.encode()
    # encode_data = base64.b64encode(raw)
    # print(type(encode_data))
    # send_mail("slepcov_oleg@mail.ru", "2345", "body", raw, "Cate.jpg")
    main()
    # email = request.GET.get('to_email')
    # head = request.GET.get('head')
    # body = request.GET.get('body')
    # f_data = request.GET.get('f_data')
    # f_name = request.GET.get('f_name')























