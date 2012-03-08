from dhouse.models import *
from django.contrib import admin

# class UserAdmin(admin.ModelAdmin):
#     fieldsets = [
#     	(None, {'fields':['name']}),
#     	('User Info', {'fields':['age','gender','addr',]}),
#     	('Account Info', {'fields':['money','state','expire_date']})
#     ]

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(SalesRecord)