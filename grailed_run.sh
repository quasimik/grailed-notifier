#!/bin/bash
PATH=/home/ubuntu/.local/bin:/home/ubuntu/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
cd /home/ubuntu/grailed-notifier/
python3 grailed_scraper.py && python3 grailed_comparer.py && python3 grailed_emailer.py
