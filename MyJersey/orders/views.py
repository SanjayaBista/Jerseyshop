from django.template.loader import render_to_string
from store.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem
from .forms import OrderForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
            #clearing the cart
            cart.clear()
            #launching asynchronous tasks
            order_created.delay(order.id)
            #setting order in the session
            request.session['order_id'] = order.id
            #return render(request,'order/created.html',{'order':order})
            #redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderForm()
    return render(request,'order/create.html',{'cart':cart,'form':form})
        

@staff_member_required
def admin_order_detail(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'admin/detail.html',{'order':order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('order/pdf.html',{'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response