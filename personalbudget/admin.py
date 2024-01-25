from django.contrib import admin
from .models import Expense, Category, Income, Source


# Register your models here.


class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('owner', 'item', 'category', 'description', 'cost', 'qty', 'amount', 'date')
    search_fields = ('item', 'category', 'description', 'amount', 'date')
    list_per_page = 5


class IncomesAdmin(admin.ModelAdmin):
    list_display = ('owner', 'amount', 'source', 'description', 'date')
    search_fields = ('amount', 'source', 'description', 'date')
    list_per_page = 5


admin.site.register(Expense, ExpensesAdmin)
admin.site.register(Category)
admin.site.register(Income, IncomesAdmin)
admin.site.register(Source)
