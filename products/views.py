import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, F
from functools import wraps

from .models import Product, Sale, Category, Profile


def role_required(*roles):
    """Доступ только для пользователей с указанной ролью (cashier / stockman)."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            profile = getattr(request.user, 'profile', None)
            if not profile or profile.role not in roles:
                return render(
                    request,
                    '403.html',
                    {'message': 'У вас нет прав для выполнения этого действия.'},
                    status=403,
                )
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def index(request):
    categories = Category.objects.all()
    cat_id = request.GET.get('category')

    if cat_id:
        products = Product.objects.filter(category_id=cat_id)
    else:
        products = Product.objects.all()

    try:
        data = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=3).json()
        usd_rate = data['rates']['KZT']
    except Exception:
        usd_rate = 475.0

    for p in products:
        p.price_usd = round(float(p.price) / usd_rate, 2)

    total_sales_sum = Sale.objects.aggregate(
        total=Sum(F('amount') * F('product__price'))
    )['total'] or 0

    return render(request, 'products/index.html', {
        'products': products,
        'categories': categories,
        'usd_rate': usd_rate,
        'total_sales_sum': total_sales_sum,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/detail.html', {'product': product})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password1 = request.POST.get('password1') or ''
        password2 = request.POST.get('password2') or ''
        role = request.POST.get('role')

        form_data = {'username': username, 'role': role}

        # Валидация
        if len(username) < 3:
            messages.error(request, 'Логин должен быть не короче 3 символов.')
            return render(request, 'registration/register.html', {'form_data': form_data})

        if role not in ('cashier', 'stockman'):
            messages.error(request, 'Выберите корректную должность.')
            return render(request, 'registration/register.html', {'form_data': form_data})

        if len(password1) < 6:
            messages.error(request, 'Пароль должен быть не короче 6 символов.')
            return render(request, 'registration/register.html', {'form_data': form_data})

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'registration/register.html', {'form_data': form_data})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует.')
            return render(request, 'registration/register.html', {'form_data': form_data})

        user = User.objects.create_user(username=username, password=password1)

        # Профиль создаётся сигналом, проставим роль
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        # Автоматический вход после регистрации
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('/')

        messages.success(request, f'Аккаунт {username} создан. Войдите в систему.')
        return redirect('login')

    return render(request, 'registration/register.html')


@role_required('stockman')
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        qty = request.POST.get('quantity')
        cat_id = request.POST.get('category')
        category = get_object_or_404(Category, id=cat_id)
        img = request.FILES.get('image')
        desc = request.POST.get('description')

        Product.objects.create(
            name=name,
            price=price,
            quantity=qty,
            category=category,
            image=img,
            description=desc,
        )
        messages.success(request, f'Товар "{name}" добавлен.')
        return redirect('/')

    categories = Category.objects.all()
    return render(request, 'products/add_product.html', {'categories': categories})


@role_required('cashier')
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.quantity > 0:
        product.quantity -= 1
        product.save()
        Sale.objects.create(product=product, amount=1)
        messages.success(request, f'Продажа "{product.name}" оформлена.')
    else:
        messages.error(request, 'Товара нет в наличии.')
    return redirect('/')


@role_required('stockman')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.description = request.POST.get('description')

        cat_id = request.POST.get('category')
        if cat_id:
            product.category = get_object_or_404(Category, id=cat_id)

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        messages.success(request, 'Товар обновлён.')
        return redirect('product_detail', product_id=product.pk)

    categories = Category.objects.all()
    return render(
        request,
        'products/edit_product.html',
        {'product': product, 'categories': categories},
    )
