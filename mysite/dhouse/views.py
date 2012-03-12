from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, QueryDict
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.contrib.auth.decorators import login_required
from dhouse.models import UserProfile, Product, SalesRecord, OrdersRecord
from datetime import datetime, timedelta
import os

MAX_ORDER_DAYS = 7

def index(request):
    '''
    url: /
    '''
    products_all = Product.objects.all()
    p_row = len(products_all) / 3 + 1
    products = [ [ None for c in range(3)] for r in range(p_row) ]
    for i in range(len(products_all)):
        products[i/3][i%3] = products_all[i]
    
    user = request.user

    if user.is_authenticated():
        profile = user.get_profile()
        if datetime.now() > profile.expire_date:
            profile.state = False
            profile.save()
    else:
        profile = None

    context = {
        'user': user,
        'products': products,
        'profile': profile,
    }
    return render_to_response('index.html', context)

def register(request):
    '''
    url: /register
    '''
    if request.method == 'POST':
        query_dict = request.POST
        username = query_dict['username']
        email = query_dict['email']
        password = query_dict['password']
        user = User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        profile = user.get_profile()
        profile.name = query_dict['name']
        profile.age = query_dict['age']
        profile.gender = query_dict['gender']
        profile.addr = query_dict['addr']
        profile.money = query_dict['money']
        if float(profile.money) >= 100:
            profile.state = True
        profile.save()
        if user is not None and user.is_active:
            login(request, user)
            # return render_to_response("index.html", {"login": True, "username": user.username})
            return redirect('/')
    elif request.method == 'GET':
        #print request.GET
        return render_to_response('register.html')

def signin(request):
    '''
    url: /signin
    '''
    if request.method == 'GET':
        return render_to_response('signin.html', {'next': request.GET.get('next', None)})
    elif request.method == 'POST':
        query_dict = request.POST
        username = query_dict['username']
        password = query_dict['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            #Redirect to a success page
            if user.is_active:
                login(request, user)
                next = request.POST.get('next', None)
                if next:
                    return redirect(request.POST['next'])
                else:
                    return redirect('/')
            #Redirect to another signin page and show error. (Can be done in a better way through js)
            else:
                return render_to_response('signin.html', {'next': request.POST.get('next', '/'), 'error': 'User is not active',})
        else:
            return render_to_response('signin.html', {'next': request.POST.get('next', '/'), 'error': 'Incorrect login information',})


def signout(request):
    '''
    url: /signout
    '''
    logout(request)
    return redirect('/')

@login_required
def profile(request, user_id=0):
    '''
    url: /profile
    '''
    if user_id == 0 :
        rd = '/profile/%d' % request.user.pk
        return redirect(rd) 
    else:
        try:
            profile = request.user.get_profile()
        except SiteProfileNotAvailable:
            return render_to_response('signin.html', {'error': 'Profile unavaliable, login please.'})

    products_bought = Product.objects.filter(userprofile__id=profile.id)
    ors = OrdersRecord.objects.filter(user=profile)
    orders = ors.filter(state=False)
    context = {
        'user'    :   request.user,
        'profile' :   profile,
        'products_bought' :   products_bought,
        'orders' :   orders,
    }
    return render_to_response('profile.html', context)

@login_required
def buy(request, product_id=0):
    '''
    url: /buy
    url: /buy/product_id
    '''
    error = ''
    if product_id == 0:
        error = 'No product have been chosen'
        return render_to_response('error.html', {'error': error})
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        profile = user.get_profile()
        query_dict = request.POST
        number_str = query_dict['number']
        number_int = int(number_str)
        if number_int <= product.remains:
            if profile.level > 5: 
                profile.level = 5
                profile.save()
            discount = (10 - profile.level) / 10.0
            price_unit = round(product.price * discount * product.discount, 1)
            pay_all = round(number_int * price_unit, 1)
            if profile.money >= pay_all:
                SalesRecord.objects.create(user=profile, product=product, num=number_str, money=pay_all)
                profile.money -= pay_all
                product.remains -= number_int
                profile.save()
                product.save()
                # deal with level
                srs = SalesRecord.objects.filter(user=profile)
                if srs:
                    money_sum = 0
                    level = profile.level
                    for sr in srs:
                        money_sum += sr.product.price*sr.num
                    if (money_sum > (level+1)*2000) and (level <= 5):
                        profile.level += 1
                        profile.save()
            else:
                error = 'You do not have enough money'
        else:
            error = 'Remains insufficent! Please try other products'
        context = {

        }
        return redirect('/')
    elif request.method == 'GET':
        error = 'You have not provide info about product'
        return render_to_response('error.html', {'error': error})

@login_required
def order(request, product_id=0):
    '''
    url: /order
    url: /order/product_id
    '''
    error = ''
    if product_id == 0:
        error = 'No product have been chosen'
        return render_to_response('error.html', {'error': error})

    if request.method == 'GET':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        profile = user.get_profile()
        context = {
            'user': user,
            'product': product,
        }
        return render_to_response('order.html', context)
    elif request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        profile = user.get_profile()
        query_dict = request.POST
        days_str = query_dict['days']
        days_int = int(days_str)
        now = datetime.now()
        time_buy = now + timedelta(days=days_int)
        number_str = query_dict['number']
        number_int = int(number_str) 
        if number_int <= product.remains:
            if days_int <= MAX_ORDER_DAYS:
                if profile.level > 5: 
                    profile.level = 5
                    profile.save()
                discount = (10 - profile.level) / 10.0
                price_unit = round(product.price * discount * product.discount, 1)
                pay_all = round(number_int * price_unit / 2, 1)
                if profile.money >= pay_all:
                    OrdersRecord.objects.create(user=profile, product=product, num=number_str, time=now, time_buy=time_buy, money=pay_all)
                    profile.money -= pay_all
                    product.remains -= number_int
                    profile.save()
                    product.save()
                else:
                    error = 'Not enough money to order'
            else:
                error = 'Remains insufficent! Please try other products'
        return redirect('/profile')

@login_required
def confirmOrder(request, order_id=0):
    '''
    url: /confirmorder/order_id
    '''
    error = ''
    if order_id == 0:
        error = 'No order_id found'
        return redirect('error.html', {'error': error})
    order = get_object_or_404(OrdersRecord, pk=order_id)
    now = datetime.now()
    if order.time_buy >= now:   # the order does not expire
        order.state = True
        order.save()
        profile = order.user
        profile.money -= order.money
        profile.save()
        product = order.product
        number = order.num
        money = order.money * 2
        SalesRecord.objects.create(user=profile, product=product, num=number, money=money)
    else:
        product = order.product
        product.remains += order.num
        order.state = True
        order.save()
    rd = '/profile/%d' % request.user.id
    return redirect(rd)

@login_required
def cancelOrder(request, order_id=0):
    '''
    url: /cancelorder/order_id
    '''
    error = ''
    if order_id == 0:
        error = 'No order_id found'
        return redirect('error.html', {'error': error})
    order = get_object_or_404(OrdersRecord, pk=order_id)
    now = datetime.now()
    if order.time_buy >= now:   # the order does not expire
        profile = order.user
        profile.money += order.money
        product = order.product
        product.remains += order.num
        profile.save()
        product.save()
        order.delete()
    rd = '/profile/%d' % request.user.id
    return redirect(rd)

@login_required
def changeProfile(request, profile_id):
    '''
    url:change
    '''
    if request.method == 'POST':
        user = request.user
        query_dict = request.POST
        profile = user.get_profile()
        if query_dict['username']:
            user.username = query_dict['username']
        if query_dict['email']:
            user.email = query_dict['email']
        if query_dict['name']:
            profile.name = query_dict['name']
        if query_dict['age']:
            profile.age = query_dict['age']
        if query_dict['gender']:
            profile.gender = query_dict['gender']
        if query_dict['addr']:
            profile.addr = query_dict['addr']
        if query_dict['moneyadd']:
            moneyadd = float(query_dict['moneyadd'])
        else:
            moneyadd = 0.0
        money_before = profile.money
        if moneyadd > 0:
            if moneyadd >= 100.0:
                profile.state = True
                now = datetime.now()
                profile.expire_date = now.replace(year=now.year+1)
            profile.money = money_before + moneyadd

        profile.save()
        user.save()
   
        rd = '/change/%d' % profile.id
        return redirect(rd)
    else:
        return redirect('/')

def productsAvaliable(request):
    '''
    url: /productsavaliable
    '''
    products = Product.objects.filter(remains__gt=0)
    user = request.user
    if user.is_authenticated():
        profile = user.get_profile()
    else:
        profile = None
    context = {
        'user' : user,
        'products' : products,
        'profile' : profile,
    }
    return render_to_response('products.html', context);

def productsAll(request):
    '''
    url: /productsavaliable
    '''
    products = Product.objects.all()
    user = request.user
    if user.is_authenticated():
        profile = user.get_profile()
    else:
        profile = None
    context = {
        'user' : request.user,
        'products' : products,
        'profile' : profile,
    }
    return render_to_response('products.html', context);

@login_required
def charts(request):
    '''
    url: /charts [ugly hack]:should custume the admin page
    '''
    profiles = UserProfile.objects.all()

    filename = os.path.join('static', 'data', 'data.csv')

    records = open(filename, 'w')
    records.write('Categories,Apples,Pears,Oranges,Bananas\n')
    records.write('John,8,4,6,5\n')
    records.write('Jane,3,4,2,3\n')
    records.write('Joe,86,76,79,77\n')
    records.write('Janet,3,16,13,15')
    records.close()
    return render_to_response('charts.html')