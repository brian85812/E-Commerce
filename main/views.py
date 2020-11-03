from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
# Create your views here.
class IndexView(ListView):
    model = Item
    template_name = "home-page.html"
    context_object_name = 'items'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
        })
        return context

    def get_queryset(self):
        return Item.objects.all()

class IndexByCategory(ListView):
    model = Item
    template_name = "home-page.html"
    context_object_name = 'items'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(IndexByCategory, self).get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'current_category':Category.objects.get(id=self.kwargs['category_id']),
        })
        return context

    def get_queryset(self):
        category = Category.objects.get(id=self.kwargs['category_id'])  #
        return Item.objects.filter(category=category)   #

class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "數量已更新")
            return redirect("main:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "加入購物車成功！")
            return redirect("main:product", pk = pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "加入購物車成功！")
        return redirect("main:order-summary")
@login_required

def remove_from_cart(request, pk):
    item = get_object_or_404(Item, id=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            if order.items.count() == 0:
                order_qs.delete()
            messages.info(request, "商品已移除購物車！")
            return redirect("main:order-summary")
        else:
            messages.warning(request, "此商品不在購物車內")
            return redirect("main:order-summary")
    else:
        messages.warning(request, "購物車尚未有任何商品")
        return redirect("main:product", pk = pk)

class OrderSummaryView( LoginRequiredMixin,View):
     def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False)
        context = {
            'object': order
        }
        return render(self.request, 'order-summary.html', context)

@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, id=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_qs.delete()
            messages.info(request, "數量已更新")
            return redirect("main:order-summary")
        else:
            messages.warning(request, "此商品不在購物車內")
            return redirect("main:product", pk=pk)
    else:
        messages.warning(request, "購物車尚未有任何商品")
        return redirect("main:product", pk=pk)

class CheckoutView(ListView):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order':order,
            }

            return render(self.request, "checkout-page.html", context)
        except:
            messages.warning(self.request, "購物車尚未有任何商品")
            return redirect("main:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            order = Order.objects.get(user=self.request.user, ordered=False)

            order.bank_account = int(form.cleaned_data.get('bank_account'))
            order.receiver_name =  form.cleaned_data.get('receiver_name')
            order.shipping_address =  form.cleaned_data.get('shipping_address')
            order.ordered =  True
            order.save()
            return redirect("main:history-order")

        else:
            messages.warning(self.request, "請確認欄位")
            return redirect("main:checkout")

class HistoryOrderView( LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        orders = Order.objects.filter(user=self.request.user, ordered=True)
        context = {
            'orders': orders
        }
        return render(self.request, 'history-order.html', context)