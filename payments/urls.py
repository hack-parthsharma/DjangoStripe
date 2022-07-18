from django.urls import path

from payments import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),

    path('session/', views.create_checkout_session, name='session'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing/', views.manage_billing, name='billing'),

    path('message/', views.show_message, name='message'),
]