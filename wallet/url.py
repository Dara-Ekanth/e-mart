from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/<str:id>/', checkout_payment, name="home"),
    # path('reg/', reg_view, name="reg_page"),
    # path('login/', login_view, name="login_page"),
    # path('logout/', logout_user, name='logout'),
    path('success/', success, name="success"),
    path('add/balance', add_balance_to_wallet, name='add_balance'),
    path('add/success', adding_balance_success, name='add_success'),
    path('paywith/wallet', pay_with_wallet, name='partial_using_wallet'),
]
