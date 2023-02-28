from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage, message, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

def check_role_vendor(user):
    if user.role == 1:
        return True
    raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    raise PermissionDenied

def get_role_url(request):
    user = request.user
    if user.role == 1:
        return 'vendor_dashboard'
        
    if user.role == 2:
        return 'customer_dashboard'
    if user.is_admin:
        return '/admin'
    
def send_email_activation(request, user, mail_subject, email_template):
    current_site = get_current_site(request)
    from_email = settings.DEFAULT_FROM_EMAIL
    body = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': default_token_generator.make_token(user),
    })
    message = EmailMessage(subject=mail_subject, body=body, from_email=from_email, to=[user.email])
    message.content_subtype = 'html'
    message.send()
    print(user.email)
    
def send_notification(mail_subject, mail_template, context):
    print('in the send function', mail_subject)
    print('template', mail_template)
    print('context', context)
    from_email = settings.DEFAULT_FROM_EMAIL
    print(from_email)
    message = render_to_string(mail_template, context)
    
    print(message)

    if (isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    print(to_email)
    # mail = EmailMessage(mail_subject, message, from_email, to_email)
    mail = EmailMessage(subject=mail_subject, body=message, from_email=from_email, to=to_email)
    print('mail: ', mail)
    mail.content_subtype = 'html'
    mail.send()