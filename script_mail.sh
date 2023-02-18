#!/bin/bash
MY_WORK_DIR="/home/atonlab/projects/read_email_fo_bx24-"

source "$MY_WORK_DIR/venv/bin/activate"
cd "$MY_WORK_DIR"
python run_mail.py >> "$MY_WORK_DIR/logs/print/log_$(date +\%Y_\%m).log" 2>&1
