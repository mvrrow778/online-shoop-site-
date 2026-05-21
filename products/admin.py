from django.contrib import admin
from django.db.models import Sum
from .models import Category, Product, Sale, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'sale_date', 'get_price')

    def get_price(self, obj):
        return f"{obj.product.price} тг."
    get_price.short_description = 'Цена продажи'

    def changelist_view(self, request, extra_context=None):
        result = Sale.objects.aggregate(total=Sum('product__price'))
        total_sales = result['total'] or 0
        
        categories_stat = []
        for cat in Category.objects.all():
            cat_sum = Sale.objects.filter(product__category=cat).aggregate(total=Sum('product__price'))['total'] or 0
            if cat_sum > 0:
                categories_stat.append({'name': cat.name, 'total': cat_sum})

        extra_context = extra_context or {}
        extra_context['total_sales_amount'] = total_sales
        extra_context['categories_stat'] = categories_stat
        
        return super().changelist_view(request, extra_context=extra_context)

