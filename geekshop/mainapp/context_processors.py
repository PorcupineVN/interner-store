from basketapp.models import Basket

MENU_LINKS = [
    {"url": "main", "active":["main"], "name": "Домой"},
    {"url": "products:main", "active":["products:main", "products:category"], "name": "Продукты"},
    {"url": "contact", "active":["contact"], "name": "Контакты"},
]


def menu_links(request):
    return {
        'menu_links': MENU_LINKS
    }

def basket(request):
   print(f'context processor basket works')
   basket = []

   if request.user.is_authenticated:
       basket = Basket.objects.filter(user=request.user)

   return {
       'basket': basket,
   }