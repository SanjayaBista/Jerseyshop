from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@shared_task
def payment_completed(order_id):
    #task to send an email notice when ordered successfully
    order = Order.objects.get(id=order_id)
    #create invoice email
    subject = f'My Jersey Pasal - EE Invoice no. { order.id }'
    message = 'Please find invoice for your recent purchase'
    email = EmailMessage(subject,message,'admin@MyJersey.com',[order.email]) 
    #generates pdf
    html = render_to_string('order/pdf.html',{'order':order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
    #attach pdf file
    email.attach(f'order_{order.id}.pdf',out.getvalue(),'application/pdf')
    #send email
    email.send()