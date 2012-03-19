from django.conf import settings
#from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.developer.models import *
from apps.post.models import *
from apps.post.forms import *
from apps.project.forms import *
from apps.contactform.forms import *
from apps.contactform.utils import *
from django.core.context_processors import csrf
from django.contrib.auth import logout#from social_auth.models import Providers
from django.core.mail import send_mail

def common_args(request):
    """
    The common arguments for all gallery views.
    
    STATIC_URL: static url from settings
    year: the year at the time of request  
    """ 
    user = request.user if request.user.is_authenticated() else None
    developer = Developer.objects.get(user=user) if user != None else None
    args = {
                'base_template' : 'base-ajax.html' if request.is_ajax() else 'base.html',
                'developer' : developer,
                'STATIC_URL' : settings.STATIC_URL,
                'MEDIA_URL' : settings.MEDIA_URL,
                'posts' :  Post.objects.all(),
                'tags' : Tag.objects.all(),
                'projects': Project.objects.all(),
                'user' : user,
           }
    return args

def get_form(request, form_class, instance):
    if request.method == 'POST':
        print 'got here'
        if instance:
            form = form_class(request.POST, request.FILES, instance=instance)
        else:
            form = form_class(request.POST, request.FILES)
            
        if form.is_valid():
            print 'valid'
            form.save(commit=False)
            #DO SOMETHING HERE
            form.save()
            form = form_class(instance=instance)
    else:
        if instance:
            form = form_class(instance=instance)
        else:
            form = form_class()
        
    return form

def promo(request):
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        type = request.POST['type']
        now = datetime.now()
        message = """
On %s, %s sent said hey.
Contact Information:
email: %s
""" % (now, name, email) 
#        if not settings.IS_DEV:
            #send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None)
        send_mail("code.art signup from %s" % name,'%s (%s) of the, %s variety, said hey' %(name, type, email), '"%s" <%s>' % (name, email), ['cole+code.art@decode72.com'], fail_silently=False)
        send_mail("code.art contact Confirmation",  auto_response(name), '"code.art team" <code.art@decode72.com>', [email], fail_silently=False)
        return render_to_response("success.html", {"name": name ,'STATIC_URL': settings.STATIC_URL})
    if request.user.is_authenticated():
        return redirect('/foo')
    args = common_args(request)
    args['contact'] = ContactForm()
    args.update(csrf(request))
    return render_to_response("promo.html", args)

def auto_response(name):
    return """
Hi %s!,

We received your request to stay up-to-date with code.art. 
If you have no idea what we're talking about then someone probably used your email address in our contact form. 
If this is the case we most sincerely apologize.   

Cheers,

code.art + Decode72
http://code.art72.org
""" % (name)

def home(request):
    args = common_args(request)
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.developer = Developer.objects.get(user=request.user)
            post.save()
            args.update({'result': 'your post got added'})
        else:
            args.update({'result': 'your post did not validate...'})
    args.update(csrf(request))
    args.update({'post_form':PostForm()})
    args.update({'projects': Project.objects.all()})
    return render_to_response('index.html', args)

def oauth_authorize(request):
    return False
 
def login(request):
#    for p in Provider.objects.all():
#        print p
    return redirect("/auth/login/github")
 
def log_out(request):
    logout(request)
    args = common_args(request)
    return render_to_response('index.html', args)
 
def logged_in(request):
     return redirect("/profile/%s" % request.user.username)