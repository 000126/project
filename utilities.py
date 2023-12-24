from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email_sendgrid(to_email, content):
    api_key = ''
    message = Mail(
        from_email='exaple@gmail.com',
        to_email=to_email,
        subject='test email from ---',
        html_content=content,
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print("email sent successfully")
        print("status code", response.status_code)
    except Exception as e:
        print("Error", str(e)),
