"""
URL configuration for shop project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from products import views
from products.views import index, product_detail, buy_product

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('buy/<int:product_id>/', buy_product, name='buy_product'),
    path('add-product/', views.add_product, name='add_product'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),

    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change',
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
