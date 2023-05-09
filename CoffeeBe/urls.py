from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('gallery/', gallery, name='gallery'),
    path('latte/', latte, name='latte'),
    path('cappuccino/', cappuccino, name='cappuccino'),
    path('espresso/', espresso, name='espresso'),
    path('typo/', typo, name='typo'),
    path('contact/', contact, name='contact'),
    path('add_blog/', add_blog, name='add_blog'),
    path('register/', registration, name='registration'),
    path('register_submit/', register_submit, name='register_submit'),
    path('otp/', u_otp, name='otp'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('my_blogs/', my_blogs, name='my_blogs'),
    path('singleblog/<int:pk>', singleblog, name='singleblog'),
    path('add_comment/<int:blog_id>', add_comment, name='add_comment'),
    path('searched_blog/', searched_blog, name='searched_blog'),
    path('donate/<int:blog_id>', donate, name='donate'),
    path('donate/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('my_profile/', my_profile, name='my_profile'),
]