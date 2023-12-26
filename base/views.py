from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import User, Product, Testimonial
from .forms import ProductForm, UserForm, MyUserCreationForm, TestimonialForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': page}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'login_register.html', {'form': form})
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(
        Q(name__icontains=q) | 
        Q(category__icontains=q) | 
        Q(brand__icontains=q)
    )
    testimonials = Testimonial.objects.all()
    context = {'products': products, 'testimonials': testimonials}
    return render(request, 'home.html', context)

def product(request, pk):
    product = Product.objects.get(id=pk)
    related = Product.objects.all()
    context = {'products': product, 'related': related}
    return render(request, 'product-details.html', context)

def products(request):
    products = Product.objects.all()
    users = User.objects.all()
    context = {'products': products, 'users': users}
    return render(request, 'product.html', context)

@login_required(login_url='login')
def productsAdmin(request):
    products = Product.objects.all()
    users = User.objects.all()
    context = {'products': products, 'users': users}
    return render(request, 'product-admin.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    products = user.product_set.all()
    context = {'user': user, 'products': products,
            }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'update-user.html', {'form': form})

def testimonials(request):
    testimonials = Testimonial.objects.get()
    testimonees = testimonials.user
    context = {'testimonials': testimonials, 'them': testimonees}
    return render(request, 'testimonials.html', context)

@login_required(login_url='home')
def viewCart(request, pk):
    products_list = User.products  # Assuming User model has a 'products' field containing product IDs
    sub_total = 0
    products = Product.objects.filter(id__in=products_list)
    #products = User.objects.get(pk=request.user.id).products
    for product in products:
        product_price = float(product.price)
        sub_total += product_price
    tax = sub_total * 0.3
    net_total = sub_total + tax
    context = {'products': products, 'list': products_list, 'sub_total': round(sub_total), 'tax': round(tax), 'net': round(net_total)}
    return render(request, 'cart.html', context)
# @login_required(login_url='home')
# def viewCart(request):
#     # Get the IDs of all products in the cart.
#     cart_product_ids = User.products.all()

#     # Fetch all products from the database whose IDs belong to the cart.
#     products = Product.objects.filter(id__in=cart_product_ids)

#     # Render the cart template with the products.
#     context = {'products': products}
#     return render(request, 'cart.html', context)


@login_required(login_url='login')
def addProduct(request):
    form = ProductForm()
    context = {'form': form}
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'add-product.html', context)

@login_required(login_url='login')
def addCart(request, pk):
    cart = []
    sub_total = 0
    cart.append(Product.objects.get(id=pk))
    User.products.append(pk)
    #User.objects.filter(pk=request.user.id).update(products=User.products)
    cart_1 = User.products
    #User.save(self=cart_1)
    products = Product.objects.filter(id__in=cart_1)
    for product in products:
        product_price = float(product.price)
        sub_total += product_price
    tax = sub_total * 0.3
    net_total = sub_total + tax
    context = {'products': products,
                'cart': cart,
                'sub_total': round(sub_total),
                'tax': round(tax),
                'net': round(net_total)}
    return render(request, 'cart.html', context, status=200)

@login_required(login_url='login')
def removeCart(request, pk):
    sub_total = 0
    cart_1 = User.products
    cart_1.remove(pk)
    products = Product.objects.filter(id__in=cart_1)
    for product in products:
        product_price = float(product.price)
        sub_total += product_price
    tax = sub_total * 0.3
    net_total = sub_total + tax
    context = {'products': products,
                'sub_total': round(sub_total),
                'tax': round(tax),
                'net': round(net_total)}
    return render(request, 'cart.html', context, status=200)

@login_required(login_url='login')
def removeProduct(request, pk):
    products = Product.objects.get(id=pk)
    if request.user.username != 'admin':
        return HttpResponse('Your are not allowed to perform this action')
    products.delete()
    return redirect('admin-view')

@login_required(login_url='login')
def addTestimonial(request):
    form = TestimonialForm()
    form.user = request.user.username.lower
    context = {'form': form}
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    testimonials = Testimonial.objects.all()
    context = {'testimonials': testimonials, 'form': form}
    return render(request, 'add-testimonial.html', context)



