from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from admin.models import *

def honssa_main(request):
    product_list = product_tbl.objects.all()
    products = []
    for i in range(8):
        products.append(product_list[i])
    return render(request, 'honssauser/main.html', {'product': products})

def honssa_category(request, category):
    category = category

    if category == '에어컨':
        category = '에어컨/냉풍기'
    elif category == '에어프라이어':
        category = '에어프라이어/튀김기'

    if category == '주방용품':
        product = product_tbl.objects.filter(Q(product_category='냉장고') | Q(product_category='에어프라이어/튀김기'))
    elif category == '생활용품':
        product = product_tbl.objects.filter(product_category='에어컨/냉풍기')
    elif category == '청소용품':
        product = product_tbl.objects.filter(Q(product_category='세탁기') | Q(product_category='청소기'))
    else:
        product = product_tbl.objects.filter(product_category__icontains= category)

    content = {'category': category, 'product': product}
    return render(request, 'honssauser/category.html', content)

def honssa_cart(request):
    id = request.user.id
    member = member_tbl.objects.get(id= id)
    total_price = 0
    if cart_tbl.objects.filter(member_number = member.id):
        cart = cart_tbl.objects.filter(member_number = member.id)
    else:
        cart = None

    if cart:
        for i in cart:
            total_price += i.cart_product_price

    auth_user = User.objects.get(id= id)
    post_number = auth_user.first_name

    context = {'cart': cart, 'member': member, 'total': total_price, 'post_number': post_number}
    return render(request, 'honssauser/cart.html', context)

def cart_delete(request, id):
    cart = cart_tbl.objects.get(id=id)
    cart.delete()
    return redirect('../')

def honssa_payment(request):
    print(request.POST)
    cart = request.POST.getlist('cart_id')
    return render(request, 'honssauser/payment.html', {'cart': cart})

def honssa_order(request):
    if request.method == 'POST':
        if request.POST['pay_method'] == '카드':
            user = member_tbl.objects.get(member_id = request.user)
            carts = request.POST.getlist('cart')
            len_products = len(carts)
            total_price = request.POST['total_price']

            for cart in carts:
                cart = cart_tbl.objects.get(id= cart)
                product = product_tbl.objects.get(id=cart.product_number)
                new_data = order_tbl(member_id = user,
                                     product_id = product,
                                     order_price = cart.cart_product_price,
                                     order_pay_status = '결제완료',
                                     order_mathod = '카드',
                                     order_quantity = cart.cart_quantity,
                                     order_bank = '카드',
                                     order_deposit_person = '카드',
                                     order_status = '배송준비',
                                     )
                product.product_stock -= cart.cart_quantity

                product.save()
                new_data.save()
                cart.delete()
            content = {'total_price': total_price, 'member': user, 'len': len_products}

        else:
            user = member_tbl.objects.get(member_id=request.user)
            carts = request.POST.getlist('cart')
            len_products = len(carts)
            total_price = 0

            for cart in carts:
                cart = cart_tbl.objects.get(id=cart)
                product = product_tbl.objects.get(id=cart.product_number.id)
                total_price += cart.cart_product_price
                new_data = order_tbl(member_id=user,
                                     product_id=product,
                                     order_price=cart.cart_product_price,
                                     order_pay_status = '결제전',
                                     order_mathod = '계좌',
                                     order_quantity = cart.cart_quantity,
                                     order_bank = '결제자 은행?',
                                     order_deposit_person = '결제자 이흠?',
                                     order_status = '결제전',
                                     )
                product.product_stock -= cart.cart_quantity

                product.save()
                new_data.save()
                cart.delete()

            content = {'total_price': total_price, 'member': user, 'len': len_products}

        return render(request, 'honssauser/order.html', content)
    return render(request, 'honssauser/order.html', {})

def honssa_create(request):
    cart_list = request.POST.getlist('cart')
    member = member_tbl.objects.get(member_id=request.user)

    price = 0
    for cart_id in cart_list:
        cart = cart_tbl.objects.get(id = cart_id)
        price += cart.cart_product_price

    content = {'price': price, 'member': member, 'cart_list': cart_list}
    return render(request, 'honssauser/create.html', content)
    # 위 괄호에 들어갈것'cart':cart, 'form':form

def product_detail(request, id):
    product = product_tbl.objects.get(id = id)
    return render(request, 'honssauser/product-detail.html', {'product':product})

def cart_insert(requset):
    user = member_tbl.objects.get(member_id=requset.user)
    product = product_tbl.objects.get(id=requset.POST['product'])
    quantity = requset.POST['quantity']
    price = product.product_Price * int(quantity)
    print(user, product, quantity, price)
    cart = cart_tbl(cart_product_price= price,
                 cart_quantity= quantity,
                 member_number= user,
                 product_number= product)
    cart.save()
    return redirect('honssauser:cart')


# Create your views here.
