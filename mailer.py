from flask import Flask, render_template, request
from email.message import EmailMessage
import ssl
import smtplib
import os
import csv
import urllib.parse
import pandas as pd

app = Flask(__name__)

def send_email(email_sender, email_receiver, subject, body, attachment_filename, attachment_content):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add the CSV file as an attachment
    em.add_attachment(attachment_content, 'text/csv', filename=attachment_filename)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, 'rkzm pwlz ltga vvhp')  # Replace 'your_password' with your actual Gmail password
        smtp.send_message(em)

# @app.route("/")
# def index():
#     return render_template("index.html")

@app.route("/", methods=["POST","GET"])
def trigger_email():
    # print('-------------------------------------')
    # print(csv_data)
    csv_data_encoded = request.args.get('csv_data', None)
    # if csv_data_encoded:
        # Decode the CSV data
    csv_data = urllib.parse.unquote(csv_data_encoded)
        # Convert the CSV data back to a DataFrame
        # df = pd.read_csv(pd.compat.StringIO(csv_data_decoded))
    # csv_data = pd.compat.StringIO(csv_data_decoded)
    # print(csv_data)

    email_sender = 'testdevelopment25@gmail.com'
    email_receiver = '1ms20is004@gmail.com'
    subject = 'CSV File via Email'
    body = 'Please find the attached Fitness Report.'
    # print(csv_data[0][0])

    # csv_data = [['Name', 'Age'],
    #             ['John', '25'],
    #             ['Alice', '30']]
    # with open('user_data.csv', 'w', newline='') as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     csv_writer.writerows(csv_data)

    # # Read the CSV file content
    # with open('user_data.csv', 'r') as file:
    #     attachment_content = file.read()

    with open('user_data.csv', 'w') as file:
        file.write(csv_data)
    with open('user_data.csv', 'r') as file:
        attachment_content = file.read()

    send_email(email_sender, email_receiver, subject, body, 'user_data.csv', attachment_content)
    
    # Remove the uploaded CSV file after sending email
    os.remove('user_data.csv')

    return "<h2>Email sent successfully!</h2>"

if __name__ == "__main__":
    app.run(port=3000, debug=True)
