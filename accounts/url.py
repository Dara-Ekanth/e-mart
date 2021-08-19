from django.urls import path
from . import views

urlpatterns = [path('hello/', views.hello_world, name='hello'),
               path('login/', views.login_views, name='login_page'),
               path('login/', views.login_views, name='accounts_login'),
               path('register/', views.register_views, name='register_page'),
               path('logout/', views.logout_view, name='logout_page'),
               path('route/settings/', views.settings_view, name='settings'),
               path('update/profile/picture', views.update_profile_view, name="update_profile_pic"),
               path('update/password/', views.update_password.as_view(template_name="accounts/update_password.html"),
                    name="update_password"),
               ]
