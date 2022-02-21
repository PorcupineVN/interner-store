from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory

MENU_LINKS = [
    {"url": "main", "active":["main"], "name": "Домой"},
    {"url": "products:main", "active":["products:main", "products:category"], "name": "Продукты"},
    {"url": "contact", "active":["contact"], "name": "Контакты"},
]
def index(request):
    products = Product.objects.all()[:4]
    return render(request, "mainapp/index.html", context={
        "title":"Главная",
        "menu_links": MENU_LINKS,
        "products": products, 
    })

def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'title':'Контакты',
        'menu_links': MENU_LINKS, 
    })

def products(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()[:4]
    return render(
        request, 
        'mainapp/products.html', 
        context={
        'title':'Продукты',
        'products':products,
        'menu_links': MENU_LINKS,
        'categories': categories, 
        },
    )

def category(request, pk):
    categories = ProductCategory.objects.all()
    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category=category)
    return render(
        request, 
        'mainapp/products.html', 
        context={
            'title':'Продукты',
            'products':products,
            'menu_links': MENU_LINKS,
            'categories': categories, 
        },
    )