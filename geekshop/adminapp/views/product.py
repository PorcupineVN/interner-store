from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory
from adminapp.utils import superuser_required

@superuser_required
def product_create(request):
    pass


@superuser_required
def products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category=category).order_by('id')

    return render(request, 'adminapp/product/products.html', context={
        'title': 'Продукты',
        'category': category,
        'objects': products,
    })


@superuser_required
def product_read(request):
    pass

@superuser_required
def product_update(request):
    pass


@superuser_required
def product_delete(request):
    pass
