import random
from functools import lru_cache
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.cache import cache_page
from .models import Product, ProductCategory





def index(request):
    products = Product.objects.all()[:4]
    return render(
        request, 
        "mainapp/index.html", 
        context={
        "title":"Главная",
        "products": products, 
        },
    )

def get_hot_product(queryset):
    return random.choice(queryset)

def get_categories():
    if settings.LOW_CACHE:
        KEY = 'all_categories'
        categories = cache.get(KEY)
        if not categories:
            categories = ProductCategory.objects.all()
            cache.set(KEY, categories)
        return categories 
    else:
        return ProductCategory.objects.all()

def products(request):
    categories = get_categories()
    products = Product.objects.all()
    hot_product = get_hot_product(products)

    return render(
        request, 
        'mainapp/products.html', 
        context={
        'title':'Продукты',
        'products':products.exclude(pk=hot_product.pk)[:4],
        'hot_product': hot_product,
        'categories': categories, 
        },
    )

@lru_cache
def get_products(category_id):
    return Product.objects.filter(category_id=category_id)


def category(request, category_id, page=1):
    categories = ProductCategory.objects.all()
    category = get_object_or_404(ProductCategory, id=category_id)
    products = get_products(category_id)
    hot_product = get_hot_product(products)
    paginator = Paginator(products.exclude(pk=hot_product.pk), 3)
    try:
        products_page = paginator.page(page)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)


    return render(
        request, 
        'mainapp/products.html', 
        context={
            'title':'Продукты',
            'products': products_page,
            'hot_product': get_hot_product(products),
            'paginator': paginator,
            'page': products_page,
            'category' : category,
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
        'categories': categories, 
        },
    )

@cache_page(3600)
def contact(request):
    return render(
        request, 
        "mainapp/contact.html", 
        context={
        'title':'Контакты',
        },
    )
