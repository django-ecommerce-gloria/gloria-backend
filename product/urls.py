from django.urls import path, include

from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search),
    path('categories/', views.CategoriesList.as_view()),
    path('products/', views.ProductsList.as_view()),
    path('orders/', views.OrdersList.as_view()),
    path('order-items/', views.OrderItemsList.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
]