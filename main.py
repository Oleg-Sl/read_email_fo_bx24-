#!/usr/bin/python
# -*- coding: utf-8 -*-

from mail_input import mail_get
import secrets


def main():
    secret = secrets.get_secrets()
    if secret and "server" in secret and "username" in secret and "password" in secret and "countmail" in secret:
        mail_get(**secret)
    else:
        print("Отсутствует файл 'secrets.json' или данные в нем!")


if __name__ == "__main__":
    main()

