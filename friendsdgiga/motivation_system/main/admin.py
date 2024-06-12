from django.contrib import admin
from .models import Service, Order, Review

@admin.action(description='Удалить все отзывы')
def delete_all_reviews(modeladmin, request, queryset):
    Review.objects.all().delete()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'service__name', 'address')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'service', 'address')
        }),
        ('Order Details', {
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ('created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'created_at')
    search_fields = ('user__username', 'service__name', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    actions = [delete_all_reviews]  # Добавление кастомного действия
