#!/usr/bin/python
# -*- coding: utf-8 -*-
from get_mail_and_create_deal.mail_input import mail_get
from services import secrets


if __name__ == "__main__":
    secret = secrets.get_secrets()
    if secret and "server" in secret and "username" in secret and "password" in secret and "countmail" in secret:
        mail_get(**secret)
    else:
        print("Отсутствует файл 'secrets.json' или данные в нем!")

