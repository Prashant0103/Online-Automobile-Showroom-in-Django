from django.contrib import admin
from auto.models import car,contact,cart,category,company,User,Post,Order


class car_title(admin.ModelAdmin):
    list_display = ['name','category','cmp','price','image']

class user_title(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','username','is_active','last_login','date_joined','is_staff']


admin.site.unregister(User)
admin.site.register(User, user_title)
admin.site.register(car,car_title)
admin.site.register(contact)
admin.site.register(cart)
admin.site.register(category)
admin.site.register(company)
admin.site.register(Order)


class BlogAdminArea(admin.AdminSite):
    site_header = 'Blog Admin Area'
    login_template = 'blog/admin/login.html'

blog_site = BlogAdminArea(name='BlogAdmin')

blog_site.register(Post)

