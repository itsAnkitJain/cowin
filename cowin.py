import requests
import json
import smtplib
import os
from email.message import EmailMessage
from datetime import date

# Gets date in required format
today_date = date.today()
year = today_date.year
month = today_date.month
dayto = today_date.day
date = f"{dayto}-{month}-{year}"

# Setup email address and password as environment variables
EMAIL_ADDR = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

# Change with your desired district id
district_id = 143

url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
response = requests.get(url, headers=headers)
availability = response.json()

# SMTP connection for email
smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtpObj.login(EMAIL_ADDR, EMAIL_PASSWORD)

def send_email():
    """
    Sends email
    """
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDR
    msg['To'] = '<email-id>'
    msg['Subject'] = content
    msg.set_content(content)
    smtpObj.send_message(msg)

# Gets required data and sends email
for i in range(len(availability["centers"])):
    for j in range(len(availability["centers"][i]["sessions"])):
        min_age_limit = availability["centers"][i]["sessions"][j]["min_age_limit"]
        available_capacity = availability["centers"][i]["sessions"][j]["available_capacity_dose1"]
        vaccine = availability["centers"][i]["sessions"][j]["vaccine"]
        if available_capacity > 0 and min_age_limit == 18:
            name = availability["centers"][i]["name"]
            vaccine_availability_date = availability["centers"][i]["sessions"][j]["date"]
            Fee = availability["centers"][i]["fee_type"]
            content = f"Center Name: {name}; Vaccine: {vaccine}; Available: {available_capacity}; Date: {vaccine_availability_date}; Fee: {Fee}"
            send_email()
smtpObj.quit()