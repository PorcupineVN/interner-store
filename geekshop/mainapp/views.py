from django.shortcuts import render

MENU_LINKS = [
    {'url':'main', 'name':'Домой'},
    {'url':'products', 'name':'Продукты'},
    {'url':'contact', 'name':'Контакты'},
]
def index(request):
    return render(request, 'mainapp/index.html', context={
        'title':'Главная',
        'menu_links': MENU_LINKS, 
    })

def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'title':'Контакты',
        'menu_links': MENU_LINKS, 
    })

def products(request):
    return render(request, 'mainapp/products.html', context={
        'title':'Продукты',
        'menu_links': MENU_LINKS, 
    })