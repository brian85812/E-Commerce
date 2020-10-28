from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, View
# Create your views here.
class IndexView(ListView):
    model = Item
    template_name = "home-page.html"
    context_object_name = 'items'

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

    def get_context_data(self, **kwargs):
        context = super(IndexByCategory, self).get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'current_category':Category.objects.get(id=self.kwargs['category_id']),
        })
        return context

    def get_queryset(self):
        return Item.objects.all()

class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"