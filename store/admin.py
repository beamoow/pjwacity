from django.contrib import admin
from store.models import Category, Product, Profile, Purchase, Review


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=['seller','title', 'picture', 'category', 'slug', 'price', 'color', 'size', 'quantity']
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Product,ProductAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display=['user', 'Firstname','Lastname', 'email', 'DOB', 'address', 'city', 'country', 'zipcode', 'tel']
    list_editable = ['address', 'city', 'country', 'zipcode']

admin.site.register(Profile,ProfileAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display=['profile', 'product','quantity', 'coupon', 'payment' ]
    list_editable = ['product', 'quantity']

admin.site.register(Purchase,PurchaseAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display=['product', 'profile','ratings', 'comment',]

admin.site.register(Review,ReviewAdmin)

