#!/bin/bash
MY_WORK_DIR="/home/oleg/PycharmProjects/bits/mail"

source "$MY_WORK_DIR/venv/bin/activate"
cd "$MY_WORK_DIR"
python run_mail.py >> "$MY_WORK_DIR/logs/print/log_$(date +\%Y_\%m).log" 2>&1
