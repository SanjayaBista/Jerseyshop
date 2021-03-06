from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender

def main(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    context = {'category':category, 'categories':categories,'products':products}
    return render(request,'store/main.html',context)

def prod_details(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug,availibility=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product],4)
    context = {'product':product,'cart_product_form':cart_product_form,'recommended_products':recommended_products}
    return render(request,'store/prod_details.html',context)

def cart(request):
    context = {}
    return render(request,'store/cart.html',context)

def checkout(request):
    context = {}
    return render(request,'store/checkout.html',context)


