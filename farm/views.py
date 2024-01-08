from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.shortcuts import render
from .forms import RegistrationForm, CategoryForm, ProductForm, OrderConfirmationForm
from .models import UserProfile, Category, Product, LOCATION_CHOICES, Order


# Create your views here.
def about(request):

    context={

    }
    return render(request,'farm/about.html',context=context)

def blog(request):

    context={

    }
    return render(request,'farm/blog.html',context=context)\

def contact(request):

    context={

    }
    return render(request,'farm/contact.html',context=context)

def products(request):

    context={

    }
    return render(request,'farm/products.html',context=context)

def index(request):

    context={

    }
    return render(request,'farm/index.html',context=context)


User = get_user_model()

def registration(request):
    if request.user.is_authenticated:
        return redirect('buy_page')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            date_of_birth = form.cleaned_data['date_of_birth']
            location = form.cleaned_data['location']
            existing_user = User.objects.filter(username=username).exists()
            if existing_user:
                return render(request, 'farm/registration.html',
                              {'form': form, 'error_message': 'This username is already taken'})
            new_user = User.objects.create_user(username=username, email=email, password=password)
            if new_user:
                user.user = new_user
                user.phone = phone
                user.date_of_birth = date_of_birth
                user.location = location
                user.save()
                authenticated_user = authenticate(username=username, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect('buy_page')
    else:
        form = RegistrationForm()

    return render(request, 'farm/registration.html', {'form': form})



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


def calculate_delivery(location):

    if location == 'location1':
        return 200
    elif location == 'location2':
        return 250
    elif location == 'location3':
        return 150

@login_required
def buy_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    selected_category = None
    selected_products = None
    selected_product = None
    quantity = 1
    location = None
    product_price = 0
    delivery_cost = 0
    total_cost = 0
    order= None
    order_id = 0


    if request.method == 'POST':
        selected_category_id = request.POST.get('category')
        if selected_category_id:
            selected_category = get_object_or_404(Category, id=selected_category_id)
            selected_products = Product.objects.filter(category=selected_category)

        location = request.POST.get('location')

        selected_product_id = request.POST.get('product')
        if selected_product_id:
            print('Selected product')
            selected_product = get_object_or_404(Product, id=selected_product_id)
            quantity = int(request.POST.get('quantity'))

            product_price = selected_product.price * quantity
            delivery_cost = calculate_delivery(location)
            total_cost = product_price + delivery_cost

            if 'decline_delivery' in request.POST:
                total_cost = product_price
                location = None
                delivery_cost = None

            if True:
                print('Cinfirm Oreder ok')
                order = Order.objects.create(
                    user=request.user,
                    product=selected_product,
                    quantity=quantity,
                    product_price=product_price,
                    location=location,
                    delivery_cost=delivery_cost,
                    total_cost=total_cost
                )
                order.save()

                return redirect('order_success', order_id=order.order_id)



    return render(request, 'farm/buy_page.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'selected_products': selected_products,
        'selected_product': selected_product,
        'quantity': quantity,
        'location': location,
        'product_price': product_price,
        'delivery_cost': delivery_cost,
        'total_cost': total_cost,
        'order_id': order_id,
        'order_confirmation_form': OrderConfirmationForm()

    })


def order_success(request, order_id):

        order = get_object_or_404(Order, order_id=order_id)

        if request.method == 'POST':
            order_confirmation_form = OrderConfirmationForm(request.POST)
            if order_confirmation_form.is_valid():
                # Делаем что-то с подтвержденным заказом
                # Например, сохраняем в базу данных, отправляем уведомления и т.д.
                # Здесь вы можете сохранить данные о подтвержденном заказе
                messages.success(request, f"Заказ №{order.id} успешно создан!")
                return redirect('success_page')  # Редирект на страницу успешного заказа или где-то еще
        else:
            order_confirmation_form = OrderConfirmationForm()

        return render(request, 'farm/order_success.html',
                      {'order': order, 'order_confirmation_form': order_confirmation_form})






