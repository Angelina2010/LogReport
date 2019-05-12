import os

from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal
from django.utils.text import slugify
from django.db.models.signals import pre_save
from pytz import unicode
from transliterate import translit
from openpyxl import load_workbook
from num2words import num2words
from catalog.models import Category, Product, CartItem, Cart, Order, Company
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound, FileResponse
from catalog.forms import OrderForm, RegistrationForm, LoginForm, ProductForm, PasswordForm
from django.contrib.auth import login, authenticate


def index_view(request):
    return render(request, 'index.html')


def base_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'cart': cart,
        'categories': categories,
        'products': products
    }
    return render(request, 'base.html', context)


def product_view(request, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'product': product,
        'categories': categories
    }
    return render(request, 'product.html', context)


def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products_of_category = Product.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        'category': category,
        'products_of_category': products_of_category,
        'categories': categories
    }
    return render(request, 'category.html', context)


def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'cart': cart
    }
    return render(request, 'cart.html', context)


def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for i in cart.items.all():
        new_cart_total += float(i.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for i in cart.items.all():
        new_cart_total += float(i.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id=int(item_id))
    cart_item.qty = int(qty)
    cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
    cart_item.save()
    new_cart_total = 0.00
    for i in cart.items.all():
        new_cart_total += float(i.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({"cart_total": cart.items.count(), "item_total": cart_item.item_total,
                         'cart_total_price': cart.cart_total})


def order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    context = {
        'cart': cart,
        'form': form
    }
    return render(request, 'order.html', context)


def make_order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    comp_id = 0
    for i in cart.items.all():
        comp_id = i.product.owner.id
        break
    form = OrderForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        comments = form.cleaned_data['comments']
        new_order = Order()
        new_order.user = request.user
        new_order.owner = Company.objects.get(id=comp_id)
        new_order.save()
        new_order.items.add(cart)
        new_order.name = name
        new_order.phone = phone
        new_order.comments = comments
        new_order.total = cart.cart_total
        new_order.save()
        slug = slugify(translit(unicode('заказ' + str(new_order.id)), reversed=True))
        new_order.slug = slug
        new_order.save()
        path = 'media/files/' + new_order.slug + '.xlsx'
        new_order.path = path
        new_order.save()
        del request.session['cart_id']
        del request.session['total']
        return HttpResponseRedirect(reverse('thanks'))


def private_str_view(request):
    comp = Company.objects.get(user=request.user)
    if not comp.is_provider:
        order = Order.objects.filter(user=request.user).order_by('-id')
    else:

        order = Order.objects.filter(owner=comp).order_by('-id')

    context = {
        'order': order
    }
    return render(request, 'private_str.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None, request.FILES)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        f_n = form.cleaned_data['first_name']
        l_n = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        post = form.cleaned_data['post']
        f_name = form.cleaned_data['full_name']
        okpo = form.cleaned_data['okpo']
        phone = form.cleaned_data['phone']
        address = form.cleaned_data['address']
        is_pr = form.cleaned_data['is_provider']
        sign = form.cleaned_data['sign']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = f_n
        new_user.last_name = l_n
        new_user.email = email
        new_user.save()
        company = Company(user=new_user, post=post, full_name=f_name, okpo=okpo, phone=phone, address=address,
                          is_provider=is_pr, sign=sign)
        company.save()

        login(request, new_user)
        return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form
    }
    return render(request, 'registration.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def add_product_view(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        # product.slug = 'product' + str(product.id)
        product = form.save(commit=False)
        product.owner = Company.objects.get(user=request.user)
        product.save()

        return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form,
    }
    return render(request, 'add_product.html', context)


def delete_product_view(request, id):
    try:
        product = Product.objects.get(id=id)
        product.available = False
        product.save()
        return HttpResponseRedirect("base")
    except Product.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def detail_order_view(request, order_slug):
    order = Order.objects.get(slug=order_slug)
    comp = Company.objects.get(user=request.user)
    context = {
        'order': order,
        'comp': comp
    }
    return render(request, 'detail_order.html', context)


def form_doc_view(request, slug, id):
    order = Order.objects.get(id=id)
    path = order.path
    comp = Company.objects.get(user=order.user)
    wb = load_workbook('media/files/sample.xlsx')
    sheet = wb['Store']
    # val = sheet['AD26'].value
    sheet['A7'] = order.owner.full_name + ' ' + order.owner.address + ' ' + str(order.owner.phone)
    sheet['A9'] = order.owner.address
    sheet['L12'] = comp.full_name + ' ' + comp.address + ' ' + str(comp.phone)
    sheet['I14'] = order.owner.full_name + ' ' + order.owner.address + ' ' + str(order.owner.phone)
    sheet['I16'] = comp.full_name + ' ' + comp.address + ' ' + str(comp.phone)
    sheet['I18'] = 'заказ'
    sheet['AX26'] = order.id
    sheet['BI26'] = str(order.date)[:-22]
    sheet['CF13'] = order.owner.okpo
    sheet['CF7'] = order.owner.okpo
    sheet['CF12'] = order.owner.okpo
    sheet['CF15'] = order.owner.okpo
    sheet['CF17'] = order.id
    sheet['CF19'] = str(order.date)[:-22]
    sheet['CF21'] = order.id
    sheet['CF22'] = str(order.date)[:-22]
    total_qty = 0
    n = 31
    count = 1
    for cart in order.items.all():
        for cart_item in cart.items.all():
            total_qty += cart_item.qty
            sheet['A' + str(n)] = count
            sheet['D' + str(n)] = cart_item.product.title
            sheet['X' + str(n)] = 'шт'
            sheet['AC' + str(n)] = 796
            sheet['BB' + str(n)] = cart_item.qty
            sheet['BH' + str(n)] = cart_item.product.price
            n += 1
            count += 1
    sheet['K52'] = num2words(total_qty, lang='ru')
    sheet['N57'] = num2words(int(order.total), lang='ru')
    sheet['L61'] = order.owner.post
    sheet['L65'] = order.owner.post
    sheet['AG61'] = order.owner.user.last_name + ' ' + order.owner.user.first_name[:1] + '. '
    sheet['AG63'] = order.owner.user.last_name + ' ' + order.owner.user.first_name[:1] + '. '
    sheet['AG65'] = order.owner.user.last_name + ' ' + order.owner.user.first_name[:1] + '. '
    sheet['BE63'] = comp.post
    sheet['BN65'] = comp.post
    sheet['BY63'] = comp.user.last_name + ' ' + comp.user.first_name[:1] + '. '
    sheet['CF65'] = comp.user.last_name + ' ' + comp.user.first_name[:1] + '. '
    sheet['N68'] = str(order.date)[8:10]
    sheet['BE68'] = str(order.date)[8:10]
    sheet['R68'] = str(order.date)[5:7]
    sheet['BI68'] = str(order.date)[5:7]
    sheet['AA68'] = str(order.date)[0:4]
    sheet['BR68'] = str(order.date)[0:4]
    wb.save(path)
    return FileResponse(open(path, 'rb'))
