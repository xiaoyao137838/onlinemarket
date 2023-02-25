# import smtplib
# import ssl

# smtp_server = 'smtp.gmail.com'
# port = 465

# sender = 'xiaoyao61030@gmail.com'
# password = 'Xiaoyao@1'

# context = ssl.create_default_context()

# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(sender, password)
#     print('Login successfully')

#Success
# import smtplib, ssl
# from email.message import EmailMessage

# msg = EmailMessage()
# msg.set_content("The body of the email is here. Please activate")
# msg["Subject"] = "An Email Alert"
# msg["From"] = "xiaoyao61030@outlook.com"
# msg["To"] = "xiaoyao61030@outlook.com"

# context=ssl.create_default_context()

# with smtplib.SMTP("smtp.office365.com", port=587) as smtp:
#     smtp.starttls(context=context)
#     smtp.login(msg["From"], "Xiaoyao@1")
#     # smtp.send_message(msg)
#     msg.send()

from django.core.mail import send_mail

print('try to send outlook email')
send_mail(
    'This is the activation link',
    'Please click the following link to activate the account',
    'xiaoyao61030@outlook.com',
    ['xiaoyao61030@outlook.com'],
    fail_silently=False,
)

print('Finish to send outlook email')