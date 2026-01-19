from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register', views.register, name='register'),
    path('user', views.user,name='user'),
    path('logout', views.logout, name='logout'),
    path('admin', views.admin, name='admin'),
    path('store', views.store, name='store'),
    path('store/', views.product_view, name='product_view'), 
    # Store Owner Dashboard
    path('inventory/', views.product_list, name='product_list'),
    
    # Actions (Note the <int:pk> for targeting specific products)
    path('add/', views.add_product, name='add_product'),
    path('update/<int:pk>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    # User side
    path('store/', views.product_view, name='product_view'),
]
 



