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


if __name__ == "__main__":
    main()
