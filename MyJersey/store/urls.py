from django.urls import path
from . import views
app_name = 'store'

urlpatterns = [
    path('',views.main,name='main'),
    path('<slug:category_slug>/',views.main,name='prod_list_by_category'),
    path('<int:id>/<slug:slug>/',views.prod_details,name="prod_details"),
    path("cart/",views.cart, name="cart"),
    path('checkout/',views.checkout,name="checkout")
]
