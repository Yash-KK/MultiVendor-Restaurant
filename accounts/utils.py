from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
# Helper functions

def detect_user(user):
    url_to_redirect = None
    if user.role == 1:
        url_to_redirect = 'vendor-dashboard'
    elif user.role == 2:
        url_to_redirect = 'customer-dashboard'
    elif user.role == None and user.is_superadmin:
        url_to_redirect = '/admin'
    return url_to_redirect

def send_verification_mail(request,user):
    current_site = get_current_site(request)
    mail_subject = 'Please activate your Account'
    message = render_to_string('accounts/emails/accVerification.html', {
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, 'FoodOnline' ,to=[to_email])
    mail.send()
    
def send_reset_password_mail(request,user):
    current_site = get_current_site(request)
    mail_subject = 'Reset your Password'
    message = render_to_string('accounts/emails/resetPassword.html', {
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, 'FoodOnline' ,to=[to_email])
    mail.send()
    
def vendor_is_approved_mail(user):
    # current_site = get_current_site(request)
    mail_subject = 'Account Approved!'
    message = render_to_string('accounts/emails/is_approved.html',{
        'user':user,
        # 'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()



def vendor_is_not_approved_mail(user):
    # current_site = get_current_site(request)
    mail_subject = 'Account not Approved!'
    message = render_to_string('accounts/emails/is_not_approved.html',{
        'user':user,
        # 'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()

def order_confirmed_email(user, email,order_number, trans_id):
    # current_site = get_current_site(request)
    mail_subject = 'Ordered Confirmed'
    message = render_to_string('orders/emails/order_confirmed.html',{
        'user':user,
        # 'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        
        'order_number': order_number,
        'trans_id': trans_id
        
    })
    to_email = email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()
    
    
    
def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png','.jpg','.jpeg','.PNG','.JPG','.JPEG']
    if not ext in valid_extensions:
        raise ValidationError(u'Unsupported File extension. Allowed extension:' + str(valid_extensions))    
    


     