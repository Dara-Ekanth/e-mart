from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from .models import *
from .filters import *
from .forms import *
from django.contrib import messages


# Create your views here.
def ordered_item(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    myfilter = productfilter(request.GET, queryset=products)
    products = myfilter.qs
    context = {'products': products, 'cartItems': cartItems, 'myfilter': myfilter}
    return render(request, 'store/ordered_item.html', context)


@login_required(login_url='login_page')
def product_info(request, id):
    product = Product.objects.get(id=id)
    review = Review.objects.filter(product_id=id)
    context = {'product': product,'review':review}
    print(product.name, product.price)
    return render(request, 'store/product_info.html', context=context)


@login_required(login_url='login_page')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        print(items)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


@login_required(login_url='login_page')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        print(items)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


@login_required(login_url='login_page')
def updateItem(request):
    data = json.loads(request.body)
    print(data)
    productId = data.get('ProductId')
    action = data.get('action')
    print('Action:', action)
    print('ProductId:', productId)
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def prev_orders(request):
    prev_ord = Order.objects.filter(customer=request.user)
    context = {'prev_ord': prev_ord}
    return render(request, 'store/prev_orders.html', context)


def prev_items(request, id):
    prev_item = OrderItem.objects.filter(order_id=id)
    #product = OrderItem.objects.get(order_id=id)
    context = {'prev_item': prev_item}
    return render(request, 'store/prev_items.html', context)

def review_items(request,id):
    #This is to check if user is writing review before ordering
    orders_by_the_customer = Order.objects.filter(customer=request.user,paid=False)
    checking_in_order_items = OrderItem.objects.filter(product_id=id,order__in=orders_by_the_customer)
    print(checking_in_order_items,"checking order items")
    if len(checking_in_order_items)>=1:
        message = "You didn't order yet or your payment is not yet completed."
        messages.error(request,message)
        return redirect('prev_orders')
    current_form = review_form()
    #For updating the review written
    try:
        update_review = Review.objects.get(product_id=id,customer=request.user)
        print(update_review,"update review")
        if update_review:
            current_form = review_form(instance=update_review)
    except Exception as e:
        message = "Your review is Valuble for us"
        messages.success(request,message)
    if request.method == 'POST':
        current_form = review_form(request.POST)
        if current_form.is_valid():
            try:
                is_review_exist = Review.objects.get(customer=request.user,product_id=id)
                is_review_exist.content = current_form.cleaned_data.get('content')
                is_review_exist.save()
            except:
                Review.objects.create(customer=request.user,product_id=id,content=current_form.cleaned_data.get('content'))
            return redirect('prev_orders')
        else:
            message = "Task Creation Failed."
            messages.error(request, message)
    context = {'form': current_form}

    return render(request,'store/review_items.html',context)
