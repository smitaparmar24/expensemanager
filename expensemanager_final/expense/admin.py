from django.contrib import admin
from .models import Expense
from .models import Category,SubCategory

# Register your models here.
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(SubCategory)
