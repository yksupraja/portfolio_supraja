from flask import Flask, render_template, request
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

def save_contact_info(data):
    with open('contact_data.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')

def send_email(subject, body):
    # Configure the email settings (replace with your own SMTP server details)
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username='gdharanids@gmail.com'
    smtp_password = 'ainnswwpbmkuhsyd'
    sender_email = 'gdharanids@gmail.com'
    receiver_email = 'dharani.21iamos121@iadc.ac.in'

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add the HTML table to the email body
    message.attach(MIMEText(body, 'html'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        contact_data = {
            'Name': name,
            'Email': email,
            'Subject': subject,
            'Message': message
        }

        save_contact_info(contact_data)

        # Prepare the email table
        email_table = f'''
            <table>
                <tr><th>Name</th><td>{name}</td></tr>
                <tr><th>Email</th><td>{email}</td></tr>
                <tr><th>Subject</th><td>{subject}</td></tr>
                <tr><th>Message</th><td>{message}</td></tr>
            </table>
        '''

        # Send the email
        send_email(subject, email_table)

        return 'Thank you! Your message has been sent.'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)