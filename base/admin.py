from django.contrib import admin

# Register your models here.
from .models import Testimonial, Product, User

admin.site.register(User)
admin.site.register(Testimonial)
admin.site.register(Product)