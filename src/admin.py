from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import User, Product, Category, Order, OrderItem, Payment, Address,SpecialOfferProduct

# Register your models here.
admin.site.site_header = 'Grocery Shoppy Admin'
admin.site.index_title = 'Admin Panel Grocery Shoppy'


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'),
         {'fields': ('name',)}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important Dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'confirm_password')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(SpecialOfferProduct)
