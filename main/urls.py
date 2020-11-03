from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('category/<int:category_id>',views.IndexByCategory.as_view(), name='index_by_category'),
    path('product/<int:pk>/', views.ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('remove-item-from-cart/<int:pk>/', views.remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('checkout/', views.CheckoutView.as_view(),name='checkout'),
    path('history-order/', views.HistoryOrderView.as_view(), name='history-order'),
]