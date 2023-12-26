from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Product, User, Testimonial

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'avatar', 'price', 'category', 'brand']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email']

class TestimonialForm(ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'