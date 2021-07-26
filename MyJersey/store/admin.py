from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['name','slug','price','availibility','created','updated']
    list_filter = ['created','availibility','updated']
    list_editable = ['price','availibility']
    prepopulated_fields = {'slug':('name',)}