from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,To
import random, string 

def send_mail(email, code):
    message = Mail(
        from_email='bbnam159@gmail.com',
        to_emails= To(email),
        subject='Forgot PassWord',
        html_content= code)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def random_code(length):
   letters = string.hexdigits
   return ''.join(random.choice(letters) for i in range(length))
