from django.contrib import admin
from django.urls import path,re_path, include
from auto import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from auto.admin import blog_site



urlpatterns = [
    
    # path('admin/', blog_site.urls),
    
    path('book/<str:name>', views.bookc, name='bookc'),
    path('user_pro/', views.user_pro, name='user_pro'),
    path("all_products/",views.all_products, name="all_products"),
    path("single_product",views.single_product, name="single_product"),
    path('admin/', admin.site.urls),
    path("",views.index),
    path('cust_dashboard/',views.cust_dashboard,name='cust_dashboard'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('order_history/',views.index,name='order_history'),
    path('cart/',views.add_to_cart,name='cart'),
    path("get_cart_data",views.get_cart_data,name="get_cart_data"),
    path("change_quan",views.change_quan,name="change_quan"),
    path("forgotpass/", views.forgotpass, name="forgotpass"),
    path("reset_password", views.reset_password, name="reset_password"),
    path('check_user/', views.checku, name='check_user'),
    path('register/', views.register),
    path('about/', views.about),
    path('contact/', views.contact),
    path('Search/',views.Search),
    path('checklog/',views.check_user),
    path('logout/',views.ulogout,name='logout'),
    path('login/',views.check_user),
    path('process_payment',views.process_payment,name="process_payment"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process_payment',views.process_payment,name="process_payment"),
    path('payment_done',views.payment_done,name="payment_done"),
    path('payment_cancelled',views.payment_cancelled,name="payment_cancelled"),
    path('order_history',views.order_history,name="order_history"),

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

