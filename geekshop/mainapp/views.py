import random
from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory

MENU_LINKS = [
    {"url": "main", "active":["main"], "name": "Домой"},
    {"url": "products:main", "active":["products:main", "products:category"], "name": "Продукты"},
    {"url": "contact", "active":["contact"], "name": "Контакты"},
]



def index(request):
    products = Product.objects.all()[:4]
    return render(
        request, 
        "mainapp/index.html", 
        context={
        "title":"Главная",
        "menu_links": MENU_LINKS,
        "products": products, 
        },
    )


def get_hot_product(queryset):
    return random.choice(queryset)

def products(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    hot_product = get_hot_product(products)
    return render(
        request, 
        'mainapp/products.html', 
        context={
        'title':'Продукты',
        'products':products.exclude(pk=hot_product.pk)[:4],
        'hot_product': hot_product,
        'menu_links': MENU_LINKS,
        'categories': categories, 
        },
    )



def category(request, category_id):
    categories = ProductCategory.objects.all()
    category = get_object_or_404(ProductCategory, id=category_id)
    products = Product.objects.filter(category=category)
    hot_product = get_hot_product(products)
    return render(
        request, 
        'mainapp/products.html', 
        context={
            'title':'Продукты',
            'products':products.exclude(pk=hot_product.pk)[:4],
            'hot_product': get_hot_product(products),
            'menu_links': MENU_LINKS,
            'categories': categories, 
        },
    )


def product(request, product_id):
    products = get_object_or_404(Product, pk=product_id)
    categories = ProductCategory.objects.all()
    return render(
        request, 
        'mainapp/product.html', 
        context={
        'title':'Продукты',
        'product': product,
        'menu_links': MENU_LINKS,
        'categories': categories, 
        },
    )

def contact(request):
    return render(
        request, 
        "mainapp/contact.html", 
        context={
        'title':'Контакты',
        'menu_links': MENU_LINKS, 
        },
    )
