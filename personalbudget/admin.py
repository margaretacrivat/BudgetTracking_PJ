from django.contrib import admin
from .models import Expense, Category, Income, Source


# Register your models here.


class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('owner', 'item', 'category', 'description', 'cost', 'qty', 'amount', 'date')
    search_fields = ('item', 'category', 'description', 'amount', 'date')
    list_per_page = 7


class IncomesAdmin(admin.ModelAdmin):
    list_display = ('owner', 'source', 'description', 'amount', 'date')
    search_fields = ('source', 'description', 'amount', 'date')
    list_per_page = 7


admin.site.register(Expense, ExpensesAdmin)
admin.site.register(Category)
admin.site.register(Income, IncomesAdmin)
admin.site.register(Source)
