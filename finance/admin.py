from django.contrib import admin
from .models import Category, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'owner')
    list_filter = ('type', 'owner')
    search_fields = ('name',)

#сортировка по типу категории

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'owner')
    list_filter = ('date', 'category', 'owner')
    search_fields = ('description',)

# сортировка по дате и категории транзакции