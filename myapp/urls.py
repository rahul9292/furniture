from django.urls import path, include
from . import views
from .views import admin_order_list



urlpatterns = [
    path('', views.index, name="home"),
    path('about', views.about, name="about"),
    path('signup/', views.signup, name="signup"),
    

    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('process-order/', views.process_order, name='process_order'),
    path('dashboard/orders/', views.admin_order_list, name='admin-orders'),
    path('my-order/', views.latest_order_detail, name='latest_order_detail'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search_results, name='search_results'),
    path('contact_us', views.contact_us, name="contactus"),
    
    
   
]
