from unicodedata import category
from django.shortcuts import render
from .models import Product, ProductCategory

MENU_LINKS = [
    {'url':'main', 'name':'Домой'},
    {'url':'products:products', 'name':'Продукты'},
    {'url':'contact', 'name':'Контакты'},
]
def index(request):
    products = Product.objects.all()[:4]
    return render(request, 'mainapp/index.html', context={
        'title':'Главная',
        'menu_links': MENU_LINKS,
        'products': products, 
    })

def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'title':'Контакты',
        'menu_links': MENU_LINKS, 
    })

def products(request):
    categories = ProductCategory.objects.all()
    return render(
        request, 
        'mainapp/products.html', 
        context={
        'title':'Продукты',
        'products':[],
        'menu_links': MENU_LINKS,
        'categories': categories, 
        },
    )

def category(request, pk):
    return products(request)