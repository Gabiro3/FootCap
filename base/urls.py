from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('product/<str:pk>/', views.product, name="product"),
    path('products/', views.products, name="products"),
    path('adminview/', views.productsAdmin, name="admin-view"),
    path('addproduct/', views.addProduct, name="add-product"),
    path('removeproduct/<str:pk>/', views.removeProduct, name="remove-product"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-profile/', views.updateUser, name="update-profile"),
    path('cart/<str:pk>/', views.viewCart, name="cart"),
    path('viewcart/<str:pk>/', views.addCart, name="viewcart"),
    path('removecart/<str:pk>/', views.removeCart, name="remove-cart"),
    path('testimonial/', views.addTestimonial, name="testimonial"),
    #Contact url and products url
]