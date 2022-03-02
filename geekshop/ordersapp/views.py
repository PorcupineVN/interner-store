from django.shortcuts import render
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.http.response import HttpResponseBadRequest
from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderForm, OrderItemForm


class OrderList(ListView):
   model = Order

   def get_queryset(self):
       return Order.objects.filter(user=self.request.user)

class OrderEditMixin:
    def make_formset(self, instance=None):
        OrderFormSet = inlineformset_factory(Order, OrderItem, \
                                            form=OrderItemForm, extra=1)
        formset = OrderFormSet(instance=instance)
        if self.request.POST:
           formset = OrderFormSet(self.request.POST, instance=instance)
        else:
           if not instance: 
               basket_items = self.request.user.basket.all()
               if len(basket_items):
                    OrderFormSet = inlineformset_factory(Order, OrderItem, \
                                        form=OrderItemForm, extra=len(basket_items))
                    formset = OrderFormSet()
                    for num, form in enumerate(formset.forms):
                        form.initial['product'] = basket_items[num].product
                        form.initial['quantity'] = basket_items[num].quantity
                    basket_items.delete()
                    
        return formset

    def save_formset(self, form, formset):
        with transaction.atomic():
           form.instance.user = self.request.user
           self.object = form.save()
           if formset.is_valid():
               formset.instance = self.object
               formset.save()

       # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
           self.object.delete()

class OrderCreate(OrderEditMixin,CreateView):
   model = Order
   form_class = OrderForm
   fields = []
   success_url = reverse_lazy('ordersapp:orders_list')

   def get_context_data(self, **kwargs):
       data = super(OrderCreate, self).get_context_data(**kwargs)
       data['orderitems'] = self.make_formset()
       return data

   def form_valid(self, form):
       context = self.get_context_data()
       orderitems = context['orderitems']
       self.save_formset(form, orderitems)

       return super(OrderCreate, self).form_valid(form)

class OrderUpdate(OrderEditMixin, UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('ordersapp:orders_list')
    def get_context_data(self, **kwargs):
       data = super(OrderUpdate, self).get_context_data(**kwargs)
       data['orderitems'] = self.make_formset(instance=self.object)
       return data

    def form_valid(self, form):
       context = self.get_context_data()
       orderitems = context['orderitems']
       self.save_formset(form, orderitems)

       return super(OrderUpdate, self).form_valid(form)

class OrderDelete(DeleteView):
   model = Order
   success_url = reverse_lazy('ordersapp:orders_list')



class OrderDetail(DetailView):
   model = Order

   def get_context_data(self, **kwargs):
       context = super(OrderList, self).get_context_data(**kwargs)
       context['title'] = 'заказ/просмотр'
       return context


def order_forming_complete(request, pk):
   orders = Order.objects.filter(user = request.user)
   order = get_object_or_404(orders, pk=pk)
   if order.status != Order.CREATED:
       return HttpResponseBadRequest
   order.status = Order.IN_PROCESSING
   order.save()

   return HttpResponseRedirect(reverse('ordersapp:orders_list'))