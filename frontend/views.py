from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from rev.models import Service, Review, Cart

def home(request):
    services = Service.objects.all()[:6]  # Show latest 6 services
    return render(request, 'frontend/home.html', {'services': services})

def services_list(request):
    services = Service.objects.all()
    return render(request, 'frontend/services.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    reviews = Review.objects.filter(service=service)
    user_review = None
    in_cart = False
    if request.user.is_authenticated:
        user_review = Review.objects.filter(service=service, user=request.user).first()
        in_cart = Cart.objects.filter(service=service, user=request.user).exists()
    return render(request, 'frontend/service_detail.html', {
        'service': service,
        'reviews': reviews,
        'user_review': user_review,
        'in_cart': in_cart,
    })

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('service')
    return render(request, 'frontend/cart.html', {'cart_items': cart_items})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'frontend/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def add_to_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    Cart.objects.get_or_create(user=request.user, service=service)
    messages.success(request, f'{service.name} added to cart.')
    return redirect('service_detail', service_id=service_id)

@login_required
def add_review(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.update_or_create(
            user=request.user,
            service=service,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Review added successfully.')
    return redirect('service_detail', service_id=service_id)

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, f'{cart_item.service.name} removed from cart.')
    return redirect('cart')

@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).select_related('service')
    return render(request, 'frontend/my_reviews.html', {'reviews': reviews})
