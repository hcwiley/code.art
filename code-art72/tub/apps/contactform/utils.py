from datetime import datetime
from django.core.mail import send_mail
from django.shortcuts import Http404, HttpResponse
from django.template.loader import render_to_string
from forms import ContactForm

validation = {
    "invalid_email" : render_to_string("invalid-email.html"),
    "required_email" : render_to_string("required-email.html"),
    "required_message" : render_to_string("required-message.html"),
    "required_name" : render_to_string("required-name.html"),
}

def render_subject(data):
    """
    Render the subject line using the subject.txt template.
    Collapses rendered to one line and removes leading and trailing whitespace.
    data - expected to be cleaned form data
    """
    subject = render_to_string("subject.txt", data)
    return ' '.join(subject.split())  
    
def render_message(data):
    """
    Render the message using the email-webmaster.txt template.
    data - expected to be cleaned form data
    """
    data['now'] = datetime.now()
    return render_to_string("email-webmaster.txt", data)
            
def render_sender(data):            
    """
    Return the sender in the standard email format.
    e.g. "John Doe" <john@doe.com>
    data - expected to be cleaned form data
    """
    return '<%s>' % (data['email'])
            
def submit(request, recipients=None, debug=False, redirect_url=None):
    """
    Submit the contact form request.
    
    recipients: 
        the recipients to which the rendered form will be sent
    debug:
        if True, do everything but actually send the message
    redirect_url:
        if supplied, redirect a non-POST request to this url rather than raise a 404 error
    """
    if request.method == "POST": 
        args = { 'success' : False }
        form = ContactForm(request.POST)
        if form.is_valid():
            sender = render_sender(form.cleaned_data)
            subject = render_subject(form.cleaned_data) 
            message = render_message(form.cleaned_data)
            
            if not debug:
                send_mail(subject, message, sender, recipients, fail_silently=False) #,auth_user=None, auth_password=None, connection=None)
            
            args = form.cleaned_data
            args['message'] = render_to_string('success.html', args)
            args['success'] = True
            return args
        else:
            args['message'] = render_to_string('fail.html')
            return args
    elif redirect_url:
         from django.views.generic.simple import redirect_to
         redirect_to(request, redirect_url)
    else:  
        raise Http404
    
