#!/usr/bin/env python
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

INTERVAL = os.getenv('INTERVAL', 14)
SMTP_HOST = os.getenv('SMTP_HOST', None)
SMTP_USER = os.getenv('SMTP_USER', None)
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', None)
MAIL_FROM = os.getenv('MAIL_FROM', None)
MAIL_TO = os.getenv('MAIL_TO', None)

if SMTP_HOST is None:
    print('EnvVar SMTP_HOST not set')
    exit(1)
if SMTP_USER is None:
    print('EnvVar SMTP_USER not set')
    exit(1)
if SMTP_PASSWORD is None:
    print('EnvVar SMTP_PASSWORD not set')
    exit(1)
if MAIL_FROM is None:
    print('EnvVar MAIL_FROM not set')
    exit(1)
if MAIL_TO is None:
    print('EnvVar MAIL_TO not set')
    exit(1)

msg = EmailMessage()

header = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
urls = ['https://www.1blu.de/']

target = '1,-'
hardLimit = 2
print('target-price is ' + target)

notified = None
content = ''
while True:
    for url in urls:
        if notified is not None and notified > datetime.now() - timedelta(days=int(INTERVAL)):
            continue
        print('check url: ' + url)
        website = requests.get(url, headers=header)
        htmlCode = BeautifulSoup(website.content, 'html.parser')
        vServerGroup = htmlCode.find("div", {"class": "vServerGroup"})
        if vServerGroup is None:
            continue
        price = vServerGroup.find('div', {'class': 'price_price'})
        if price is None:
            continue
        price = price.text.strip()
        if price == target:
            content = 'V-Server ist gerade für ' + target + ' verfügbar.'
            print(content)
            notified = datetime.now()
        elif float(price.replace('-', '0').replace(',', '.')) < hardLimit:
            content = 'Preis ist immer noch kleiner' + str(hardLimit) + '. Preis ist: ' + str(price)
            print(content)
        if content is None:
            continue
        msg.set_content(content)
        msg['Subject'] = 'Price-Watch'
        msg['From'] = MAIL_FROM
        msg['To'] = MAIL_TO
        s = smtplib.SMTP(SMTP_HOST)
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.send_message(msg)
        s.quit()
        content = None
