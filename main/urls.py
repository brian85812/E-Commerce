from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('category/<int:category_id>',views.IndexByCategory.as_view(), name='index_by_category'),
    path('product/<int:pk>/', views.ItemDetailView.as_view(), name='product'),
]