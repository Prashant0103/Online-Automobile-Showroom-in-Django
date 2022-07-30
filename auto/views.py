import random
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, reverse, HttpResponseRedirect
from paypal.standard.forms import PayPalPaymentsForm

from auto.forms import cont
from auto.models import car, category, cart, Order


def checku(request):
    if request.method == "GET":
        un = request.GET["uname"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")


def index(request):
    data = car.objects.all()
    cats = category.objects.all().order_by("type_of_vehicle")
    return render(request, "index.html", {"data": data, "category": cats})


def all_products(request):
    context = {}
    cats = category.objects.all().order_by("type_of_vehicle")
    context["category"] = cats
    all_products = car.objects.all().order_by('name')
    context["data"] = all_products
    if "cat" in request.GET:
        cid = request.GET["cat"]
        prd = car.objects.filter(category__id=cid)
        context["data"] = prd
        context["abcd"] = "search"
    return render(request, "Search.html", context)


def single_product(request):
    context = {}
    id = request.GET["pid"]
    print(id)
    obj = car.objects.get(id=id)
    context["product"] = obj
    return render(request, "single_product.html", context)


def about(request):
    cats = category.objects.all().order_by("type_of_vehicle")
    return render(request, 'about.html', {'category': cats})


@login_required(login_url='/')
def user_pro(request):
    cats = category.objects.all().order_by("type_of_vehicle")
    return render(request, 'user_base.html', {'category': cats})


@login_required(login_url='/')
def bookc(request, **kwargs):
    try:
        name = kwargs['name']
        data = car.objects.all().filter(name=name)
        for i in data:
            name = i.name
            image = i.image
            book = bookc(name=name, image=image)
            book.save()
            return render(request, "bookc.html", {'data': data})
    except:
        return redirect('/index/')


def cust_dashboard(request):
    cats = category.objects.all().order_by("type_of_vehicle")
    cuser = request.user
    data = User.objects.all().filter(username=cuser.username)
    return render(request, "user_pro.html", {'data': data, 'category': cats})


def change_password(request):
    cats = category.objects.all().order_by("type_of_vehicle")
    cuser = request.user
    context = {}
    context['category'] = cats
    ch = User.objects.all().filter(username=cuser.username)
    if len(ch) > 0:
        data = User.objects.all().filter(username=cuser.username)
        context["data"] = data
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request, user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request, "change_password.html", context)


def add_to_cart(request):
    cats = category.objects.all().order_by("type_of_vehicle")
    context = {}
    context['category'] = cats
    items = cart.objects.filter(user__id=request.user.id)
    context["items"] = items

    for i in items:
        V = int(20 / 100 * i.car_name.price)
        context["dis"] = V

    if request.user.is_authenticated:
        if request.method == "POST":
            pid = request.POST["pid"]
            qty = request.POST["qty"]
            is_exist = cart.objects.filter(car_name__id=pid, user__id=request.user.id)
            if len(is_exist) > 0:
                context["msz"] = "Item Already Exists in Your Cart"
                context["cls"] = "alert alert-warning"
            else:
                product = get_object_or_404(car, id=pid)
                usr = get_object_or_404(User, id=request.user.id)
                c = cart(user=usr, car_name=product, quantity=qty)
                c.save()
                context["msz"] = "{} Added in Your Cart".format(product.name)
                context["cls"] = "alert alert-success"
    else:
        context["status"] = "Please Login First to View Your Cart"
    return render(request, "cart.html", context)


def get_cart_data(request):
    items = cart.objects.filter(user__id=request.user.id)
    sale, total, quantity = 0, 0, 0
    for i in items:
        sale += float(i.car_name.price) * i.quantity
        total += float(i.car_name.price) * i.quantity
        quantity += int(i.quantity)

    res = {
        "total": total, "offer": sale, "quan": quantity,
    }
    return JsonResponse(res)


def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(cart, id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)

    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(cart, id=id)
        cart_obj.delete()
        return HttpResponse(1)


def forgotpass(request):
    context = {}
    if request.method == "POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User, username=un)
        user.set_password(pwd)
        user.save()

        login(request, user)
        if user.is_superuser:
            return redirect("/admin")
        else:
            return redirect("/cust_dashboard")
        # context["status"] = "Password Changed Successfully!!!"

    return render(request, "forgot_pass.html", context)


def reset_password(request):
    un = request.GET["username"]
    try:
        user = get_object_or_404(User, username=un)
        otp = random.randint(1000, 9999)
        msz = "Dear {} \n{} is your One Time Password (OTP) \nDo not share it with others \nThanks&Regards \nMyWebsite".format(
            user.username, otp)
        try:
            email = EmailMessage("Account Verification", msz, to=[user.email])
            email.send()
            return JsonResponse({"status": "sent", "email": user.email, "rotp": otp})
        except:
            return JsonResponse({"status": "error", "email": user.email})
    except:
        return JsonResponse({"status": "failed"})


def process_payment(request):
    items = cart.objects.filter(user_id__id=request.user.id)
    products = ""
    amt = 0
    inv = "INV10001-"
    cart_ids = ""
    p_ids = ""
    for j in items:
        products += str(j.car_name.name) + "\n"
        p_ids += str(j.car_name.id) + ","
        amt += float(j.car_name.price)
        inv += str(j.id)
        cart_ids += str(j.id) + ","

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amt),
        'item_name': products,
        'invoice': inv,
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('payment_cancelled')),
    }
    usr = User.objects.get(username=request.user.username)
    ord = Order(cust_id=usr, cart_ids=cart_ids, product_ids=p_ids)
    ord.save()
    ord.invoice_id = str(ord.id) + inv
    ord.save()
    request.session["order_id"] = ord.id

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form})


def payment_done(request):
    if "order_id" in request.session:
        order_id = request.session["order_id"]
        ord_obj = get_object_or_404(Order, id=order_id)
        ord_obj.status = True
        ord_obj.save()

        for i in ord_obj.cart_ids.split(",")[:-1]:
            cart_object = cart.objects.get(id=i)
            cart_object.status = True
            cart_object.save()
    return render(request, "payment_success.html")

def payment_cancelled(request):
    return render(request,"payment_failed.html")

def order_history(request):
    context = {}
    ch = User.objects.all().filter(id=request.user.id)
    for i in ch:
        print(i)
    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context["data"] = data

    all_orders = []
    orders = Order.objects.filter(cust_id__id=request.user.id).order_by("-id")

    for order in orders:
        products = []
        for id in order.product_ids.split(",")[:-1]:
            pro = get_object_or_404(car, id=id)
            products.append(pro)
        ord = {
            "order_id": order.id,
            "products": products,
            "invoice": order.invoice_id,
            "status": order.status,
            "date": order.processed_on,
        }

        all_orders.append(ord)
    context["order_history"] = all_orders
    return render(request,"order_history.html",context)

def edit_profile(request):
    cuser = request.user
    context = {}
    check = User.objects.all().filter(username=cuser.username)
    if len(check) > 0:
        data = User.objects.all().filter(username=cuser.username)
        context["data"] = data
    if request.method == "POST":
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        em = request.POST["email"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        context["status"] = "Changes Saved Successfully"
    return render(request, "edit_profile.html", context)


def contact(request):
    cats = category.objects.all().order_by('type_of_vehicle')
    if request.method == "POST":
        form = cont()
        if request.method == 'POST':
            form = cont(request.POST)
            if form.is_valid():
                user = form.save()
                user.save()
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                name = form.cleaned_data['name']
                registered = True
                line = f"Thank You {name}, Your message send Successfully"
                messages.success(request, line)
                return redirect('/contact')
            else:
                messages.error(request, 'something went wrong...')
    else:
        form = cont()
        return render(request, 'contact.html', {'fm': form, 'category': cats})


@login_required(login_url='/')
def ulogout(request):
    logout(request)
    messages.success(request, 'Your Logout Succesfully...')
    return redirect('/')


def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.info(request, 'Username Exist Plz Choose Differnt one...')
            return render(request, 'register.html')

        elif User.objects.filter(email=email):
            messages.info(request, 'Email Exist...')
            return render(request, 'register.html')

        elif pass1 != pass2:
            messages.info(request, 'Password Did Not Match...')
            return render(request, 'register.html')

        else:
            user = User.objects.create_user(username=username, password=pass1, first_name=fname, last_name=lname,
                                            email=email)
            user.save()
            messages.success(request, 'Your Registerd Successfully...' + username)
            return redirect('/login')

    else:
        return render(request, 'register.html')


def check_user(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = authenticate(request, username=uname, password=passw)
        if user:
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                request.session['u_name'] = user.username
                request.session['u_id'] = user.id
                request.session['u_email'] = user.email
                messages.success(request, 'Welcome ' + uname + ' Your Login Successfully')
                return redirect('/')
        else:
            messages.error(request, 'plz enter valid username and password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def Search(request):
    if request.method == 'POST':
        nm = request.POST.get('fdata')
        data = car.objects.all().filter(name=nm)
        if data:
            return render(request, 'Search.html', {'data': data})
        else:
            messages.error(request, 'Car not found....')
            return redirect('/')
    else:
        messages.error(request, 'Car not found...')
        return redirect('/')
