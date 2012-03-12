from dhouse.models import *
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['name']}),
        ('User Info', {'fields':['age','gender','addr',]}),
        ('Account Info', {'fields':['money','state','expire_date']})
    ]

class ProductAdmin(admin.ModelAdmin):
    list_display=('name', 'price', 'remains')
    search_fields = ['name']

class SalesAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'product', 'time', 'num', 'money')
    search_fields = ['name']
    date_hierarchy = 'time'

class OrdersAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'product', 'time','time_buy', 'num', 'money', 'state')
    search_fields = ['name']
    date_hierarchy = 'time'

admin.site.register(UserProfile)
admin.site.register(Product, ProductAdmin)
admin.site.register(SalesRecord, SalesAdmin)
admin.site.register(OrdersRecord, OrdersAdmin)