from django.shortcuts import render, redirect
import razorpay
from .models import *
from django.contrib import messages
from .decorators import unauthenticated_user
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from _datetime import datetime
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.models import Group
from store.models import *


#
# @unauthenticated_user
# def reg_view(request):
#     form = reg_form()
#     if request.method == 'POST':
#         form = reg_form(request.POST)
#         b = customer()
#         if form.is_valid():
#             user1 = form.save()
#             print("User saved")
#             username = form.cleaned_data.get('username')
#             group = Group.objects.get(name='user')
#             user1.groups.add(group)
#             customer.objects.create(user=user1)
#             cust = customer.objects.get(user=user1)
#             wallet.objects.create(name=cust)
#             messages.success(request, "Account created for " + username)
#             return redirect('login_page')
#         else:
#             print("User failed to register.")
#             messages.error(request, "User creation failed. ")
#             return redirect('reg_page')
#     context = {'form': form}
#     return render(request, 'wallet/registration.html', context)


# @unauthenticated_user
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # print("the id of the user is",request.user.id)
#             context = {'id': request.user.id}
#             return redirect('home')
#         else:
#             messages.error(request, "Username or password is incorrect.")
#             return render(request, 'accounts/login.html')
#     return render(request, 'wallet/login.html')


# @login_required(login_url='login_page')
# def logout_user(request):
#     logout(request)
#     return redirect('login_page')

#
# @login_required(login_url='login_page')
# def home(request):
#     form = bill_form()
#     if request.method == "POST":
#         form = bill_form(request.POST)
#         is_yes = request.POST.get('yes')
#         if form.is_valid():
#             name = form.cleaned_data.get('name')
#             amount = int(form.cleaned_data.get('amount')) * 100
#             email = form.cleaned_data.get('email')
#             print("The name is", name)
#             print("The amount is", amount)
#             client = razorpay.Client(auth=(settings.DATA_KEY, settings.PAYMENT_KEY))
#             # payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
#             # print("The payment is", payment)
#             # print("The request user is", request.user)
#
#             custom = customer.objects.get(user=request.user)
#             wallet_attrb = wallet.objects.get(name=custom)
#
#             if is_yes:
#                 if amount / 100 <= wallet_attrb.balance:
#                     wallet_attrb.balance -= amount / 100
#                     wallet_attrb.save()
#                     return render(request, "wallet/wallet_success.html")
#                 else:
#                     amount -= int(wallet_attrb.balance) * 100
#                     payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
#                     receipt = bill.objects.create(name=name, amount=amount, order_id=payment['id'],
#                                                   email=email)
#                     receipt.save()
#                     context = {'payment': payment, 'amount': payment['amount'] / 100, 'paid': receipt.paid,
#                                'data_key': settings.DATA_KEY, 'balance': wallet_attrb.balance}
#                     context['amount'] = amount / 100
#
#                     return render(request, "wallet/partial_bill.html", context)
#             else:
#                 payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
#                 receipt = bill.objects.create(name=name, amount=amount, order_id=payment['id'],
#                                               email=email)
#                 receipt.save()
#                 context = {'payment': payment, 'amount': payment['amount'] / 100, 'paid': receipt.paid,
#                            'data_key': settings.DATA_KEY, 'balance': wallet_attrb.balance}
#                 return render(request, "wallet/payment.html", context)
#     return render(request, "wallet/index.html", {'form': form})

@login_required(login_url='login_page')
def checkout_payment(request, id):
    try:
        # print("checkout_payment 1")
        order_id = Order.objects.get(id=id)
        amt = order_id.get_cart_total
        name = request.user
        amount = float(amt) * 100
        order_id.amount = amount / 100
        order_id.save()
        email = request.user.email
        # print("The name is", name)
        # print("The amount is", amount)
        is_yes = request.POST.get('yes')
        client = razorpay.Client(auth=(settings.DATA_KEY, settings.PAYMENT_KEY))
        # payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        # print("The payment is", payment)
        # print("The request user is", request.user)

        # custom = customer.objects.get(user=request.user)
        wallet_attrb, creat = wallet.objects.get_or_create(name=request.user)

        if is_yes:
            if amount / 100 <= wallet_attrb.balance:
                wallet_attrb.balance -= amount / 100
                wallet_attrb.save()
                order_id.complete = True
                order_id.payment_id = "paid via wallet"
                order_id.order_id = "wallet payment"
                order_id.paid = True
                order_id.save()
                msg_plain = render_to_string('wallet/email.txt')
                msg_html = render_to_string(('wallet/email.html'))
                date = datetime.now()
                date = date.strftime("%c")
                is_sent = send_mail(f"Your payment has been received on {date} IST.", msg_plain,
                                    settings.EMAIL_HOST_USER,
                                    [email],
                                    html_message=msg_html)
                return render(request, "wallet/wallet_success.html")
            else:
                amount -= float(wallet_attrb.balance) * 100
                payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
                receipt = Order.objects.get(id=id)
                receipt.order_id = payment['id']
                # receipt.email = email
                receipt.save()
                context = {'payment': payment, 'amount': amount / 100, 'paid': receipt.paid,
                           'data_key': settings.DATA_KEY,
                           'balance': wallet_attrb.balance, 'total': wallet_attrb.balance + payment['amount'] / 100}

                return render(request, "wallet/partial_bill.html", context)
        else:
            payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
            # receipt = Order.objects.create(customer=name, amount=amount, order_id=payment['id'],
            #                                email=email)
            receipt = Order.objects.get(id=id)
            receipt.order_id = payment['id']
            # receipt.email = email
            receipt.save()
            context = {'payment': payment, 'amount': payment['amount'] / 100, 'paid': receipt.paid,
                       'data_key': settings.DATA_KEY, 'balance': wallet_attrb.balance}
            return render(request, "wallet/payment.html", context)
        return render(request, "wallet/index.html", {'form': form})


    except:
        messages.error(request, "Payment Failed")
        return redirect('default_home_name')


@login_required(login_url='login_page')
def pay_with_wallet(request):
    client = razorpay.Client(auth=(settings.DATA_KEY, settings.PAYMENT_KEY))
    if request.method == "POST":
        data = request.POST
        for key, val in data.items():
            if key == "razorpay_order_id":
                pay_id = val
                break
        tem_receipt = Order.objects.get(order_id=pay_id)
        tem_receipt.payment_id = request.POST.get("razorpay_payment_id")
        tem_receipt.paid = True
        tem_receipt.save()
        if tem_receipt.paid:
            tem_receipt.complete = True
            tem_receipt.save()
        payment = client.order.fetch(order_id=pay_id)
        if float(payment['amount_due']) == 0:
            # custom = customer.objects.get(user=request.user)
            wallet_attrb, creat = wallet.objects.get_or_create(name=request.user)
            wallet_attrb.balance = 0
            wallet_attrb.save()
    return render(request, "wallet/success.html")


@csrf_exempt
@login_required(login_url='login_page')
def success(request):
    print("success: success")
    is_sent = False
    if request.method == "POST":
        data = request.POST
        for key, val in data.items():
            if key == "razorpay_order_id":
                pay_id = val
                break
        tem_receipt = Order.objects.get(order_id=pay_id)
        tem_receipt.payment_id = request.POST.get("razorpay_payment_id")
        tem_receipt.paid = True
        tem_receipt.save()
        if tem_receipt.paid:
            tem_receipt.complete = True
            tem_receipt.save()
        amount_paid = tem_receipt.amount
        render(request, "wallet/email.html", {'amount': amount_paid})
        print("The data is printing from success", data)
        msg_plain = render_to_string('wallet/email.txt')
        msg_html = render_to_string('wallet/email.html')
        date = datetime.now()
        date = date.strftime("%c")
        is_sent = send_mail(f"Your payment has been received on {date} IST.", msg_plain, settings.EMAIL_HOST_USER,
                            [request.user.email],
                            html_message=msg_html)
        context = {'sent': is_sent, 'mail_id': request.user.email}
        if is_sent:
            return render(request, "wallet/success.html", context)

    return render(request, "wallet/success.html")


@login_required(login_url='login_page')
def add_balance_to_wallet(request):
    try:
        form = wallet_form()
        if request.method == "POST":
            form = wallet_form(request.POST)
            if form.is_valid():
                name = request.user  # form.cleaned_data.get('name')
                amount = float(form.cleaned_data.get('balance')) * 100
                client = razorpay.Client(auth=(settings.DATA_KEY, settings.PAYMENT_KEY))
                payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
                # receipt = bill.objects.filter(name=name).first()
                receipt = Order.objects.create(customer=name, amount=amount / 100, order_id=payment['id'],
                                               complete=True)
                receipt.save()
                # custom_inst = customer.objects.get(user=request.user)
                wallet_attrb, creat = wallet.objects.get_or_create(name=request.user)
                print("The wallet Balance is", wallet_attrb)
                print("The receipt of name is", receipt)
                context = {'payment': payment, 'amount': payment['amount'] / 100, 'paid': receipt.paid,
                           'data_key': settings.DATA_KEY, 'balance': wallet_attrb.balance}
                return render(request, "wallet/wallet_payment.html", context)
    except Exception as e:
        meg = str(e)
        messages.error(request, meg)
        print(e)
    wallet_attr, creat = wallet.objects.get_or_create(name=request.user)
    bal = wallet_attr.balance
    context = {'form': form, 'bal': bal}

    return render(request, 'wallet/add_balance.html', context)


@login_required(login_url='login_page')
def adding_balance_success(request):
    if request.method == "POST":
        data = request.POST
        print("The data from the adding_balance_success is", data)
        client = razorpay.Client(auth=(settings.DATA_KEY, settings.PAYMENT_KEY))

        for key, val in data.items():
            if key == "razorpay_order_id":
                pay_id = val
                break
        tem_receipt = Order.objects.get(order_id=pay_id)
        tem_receipt.payment_id = request.POST.get("razorpay_payment_id")
        tem_receipt.paid = True
        tem_receipt.paidto_wallet = True
        tem_receipt.save()
        if tem_receipt.paid:
            tem_receipt.complete = True
            tem_receipt.save()
        payment = client.order.fetch(order_id=pay_id)
        print("The payment from the adding_balance_success is", payment)
        # custom = customer.objects.get(user=request.user)
        wallet_balance = wallet.objects.get(name=request.user)
        wallet_balance.balance += payment['amount_paid'] / 100
        wallet_balance.save()
        msg_plain = render_to_string('wallet/email.txt')
        msg_html = render_to_string(('wallet/email.html'))
        date = datetime.now()
        date = date.strftime("%c")
        is_sent = send_mail(f"Your payment has been received on {date} IST.", msg_plain, settings.EMAIL_HOST_USER,
                            [request.user.email],
                            html_message=msg_html)
        # tem_receipt = bill.objects.get(order_id=pay_id)
    return render(request, "wallet/wallet_success.html")
