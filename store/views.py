from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from .models import *
from .filters import *
from .forms import *
from django.contrib import messages


# Create your views here.
# Global Variables
is_upvoter = False
is_downvoter = False
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
    global is_upvoter
    global is_downvoter
    product = Product.objects.get(id=id)
    review = Review.objects.filter(product_id=id)
    # try:
    #     review_votes = Review_votes.objects.filter(review__product_id=id)
    #     # print("review_votes",review_votes)
    #     for i in review_votes:
    #         print("this is not a magic",i)
    #     upvote_count = review_votes.upvote_count
    #     downvote_count = review_votes.downvote_count
    # except Exception as e:
    #     print(e,"Now I'm in exception++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #     upvote_count = 0
    #     downvote_count = 0
    # this_user = request.user
    # downvoters = list(review_votes.downvoters.all())
    # upvoters = list(review_votes.upvoters.all())


    context = {'product': product,'review':review}
    #print(upvote_count,downvote_count)
    #print(product.name, product.price)
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

@login_required(login_url='login_page')
def prev_orders(request):
    prev_ord = Order.objects.filter(customer=request.user)
    context = {'prev_ord': prev_ord}
    return render(request, 'store/prev_orders.html', context)

@login_required(login_url='login_page')
def prev_items(request, id):
    prev_item = OrderItem.objects.filter(order_id=id)
    order = Order.objects.get(id=id)
    context = {'prev_item': prev_item,'is_paid':order.paid}
    return render(request, 'store/prev_items.html', context)

@login_required(login_url='login_page')
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
                is_review_exist.rating = current_form.cleaned_data.get('rating')
                is_review_exist.save()
            except:
                Review.objects.create(customer=request.user,product_id=id,content=current_form.cleaned_data.get('content'),rating=current_form.cleaned_data.get('rating'))
            return redirect('prev_orders')
        else:
            message = "Unable to publish your review"
            messages.error(request, message)
    context = {'form': current_form}

    return render(request,'store/review_items.html',context)

@login_required(login_url='login_page')
def upvote_review(request,id):
    review_vote,created = Review_votes.objects.get_or_create(review_id=id)
    vdownvoters = list(review_vote.downvoters.all())
    vupvoters = list(review_vote.upvoters.all())
    this_user = request.user
    print(vdownvoters,"+++++++++++++++++++++++++++++++++++++++++++++++++")
    if this_user in vdownvoters and review_vote.down_vote > 0:
        review_vote.down_vote-=1
        review_vote.downvoters.remove(this_user)
        review_vote.save()
    if this_user in vupvoters and review_vote.up_vote > 0:
        message = "We successfully removed your like"
        messages.success(request,message)
        review_vote.up_vote-=1
        review_vote.upvoters.remove(this_user)
        review_vote.save()
        return redirect('product_description_page',id=review_vote.review.product_id)
    review_vote.up_vote+=1
    review_vote.upvoters.add(this_user)
    review_vote.save()
    return redirect('product_description_page',id=review_vote.review.product_id)

@login_required(login_url='login_page')
def downvote_review(request,id):
    review_vote,created = Review_votes.objects.get_or_create(review_id=id)
    vdownvoters = list(review_vote.downvoters.all())
    vupvoters = list(review_vote.upvoters.all())
    this_user = request.user
    print(vupvoters,"+++++++++++++++++++++++++++++++++++++++++++++++++")
    if this_user in vupvoters and review_vote.up_vote >0:
        review_vote.up_vote-=1
        review_vote.upvoters.remove(this_user)
        review_vote.save()
    if this_user in vdownvoters and review_vote.down_vote > 0:
        message = "We successfully removed your dislike"
        messages.success(request,message)
        review_vote.down_vote -=1
        review_vote.downvoters.remove(this_user)
        review_vote.save()
        return redirect('product_description_page',id=review_vote.review.product_id)
    review_vote.down_vote+=1
    review_vote.downvoters.add(this_user)
    review_vote.save()
    return redirect('product_description_page',id=review_vote.review.product_id)
