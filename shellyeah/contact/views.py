from django.shortcuts import render
from contact.forms import contact_form
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.

def contact(request):
    print(request.method)
    if request.method == 'POST':
        form = contact_form.ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            html = render_to_string('contactform.html', {
                'name': name,
                'subject': subject,
                'email': email,
                'message': message,
            })
            send_mail('The contact form subject','this is the message','eablake153@gmail.com',['eablake153@gmail.com'], html_message=html)
            content = {
                "result": "Message was successfully submitted."

            }
    else:
        form = contact_form.ContactForm()
        content = {
            "form": form,
        }

    return render(request,'contact.html',content)
    
