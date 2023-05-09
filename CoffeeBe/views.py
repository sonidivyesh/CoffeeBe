from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from django.conf import settings
from .models import *

import os
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
def home(request):
    try:
        global user_obj
        user_obj = User.objects.get(email = request.session['user_email'])
        return render(request, 'index.html', {'home': 'active', 'userdata': user_obj})
    except:
        return render(request, 'index.html', {'home': 'active'})

def about(request):
    try:
        user_obj = User.objects.get(email = request.session['user_email'])
        return render(request, 'about.html', {'about': 'active', 'userdata': user_obj})
    except: 
        return render(request, 'about.html', {'about': 'active'})

def gallery(request):
    try:
        user_obj = User.objects.get(email = request.session['user_email'])
        return render(request, 'gallery.html', {'gallery': 'active', 'userdata': user_obj})
    except:
        return render(request, 'gallery.html', {'gallery': 'active'})

def contact(request):
    try:
        user_obj = User.objects.get(email = request.session['user_email'])
        return render(request, 'contact.html', {'contact': 'active', 'userdata': user_obj})
    except:
        return render(request, 'contact.html', {'contact': 'active'})

def typo(request):
    return render(request, 'typo.html')

def latte(request):
    filtered_blogs = Blog.objects.filter(categories = 'Latte')
    try:
        user_obj = User.objects.get(email = request.session['user_email'])
        return render(request, 'latte.html', {'userdata':user_obj, 'blogs':filtered_blogs})
    except:
        return render(request, 'latte.html', {'blogs':filtered_blogs})

def cappuccino(request):
    filtered_blogs = Blog.objects.filter(categories = 'Cappuccino')
    try:
        user_obj = User.objects.get(email = request.session['user_email'])
        return render(request, 'cappuccino.html', {'userdata':user_obj, 'blogs':filtered_blogs})
    except:
        return render(request, 'cappuccino.html', {'blogs':filtered_blogs})

def espresso(request):
    filtered_blogs = Blog.objects.filter(categories = 'Espresso')
    try:
        user_obj = User.objects.get(email = request.session['user_email'])
        return render(request, 'espresso.html', {'userdata':user_obj, 'blogs':filtered_blogs})
    except:
        return render(request, 'espresso.html', {'blogs':filtered_blogs})

def registration(request):
    return render (request, 'registration.html')

def register_submit(request):
    if request.POST['passwd'] == request.POST['repasswd']:
        global g_otp, user_data
        user_data = [request.POST['first_name'],
                    request.POST['last_name'],
                    request.POST['user_name'],
                    request.POST['email'],
                    request.POST['passwd']]
        g_otp = random.randint(1000, 9999)
        send_mail('Hey !',
                  f'{g_otp} is your CoffeeBe verification code.',
                  settings.EMAIL_HOST_USER,
                  [request.POST['email']]),
        return render(request, 'otp.html')
    else:
        return render(request, 'registration.html', {'msg': 'Password do not match'})

def u_otp(request):
    try: 
        if int(request.POST['u_otp']) == g_otp:
            User.objects.create(
                    first_name = user_data[0],
                    last_name = user_data[1],
                    username = user_data[2],
                    email = user_data[3],
                    password = user_data[4])
            return render(request, 'index.html', {'userdata': user_obj, 'home': 'active'})
        else:
            return render(request, 'otp.html', {'msg': 'Invalid OTP, Enter again !!'})
    except:
        return render(request, 'registration.html')

def login(request):
    if request.method =='GET':
        return render(request, 'login.html')
    else:
        try:
            user_obj = User.objects.get(email = request.POST['email'])
            if request.POST['passwd'] == user_obj.password:
                request.session['user_email'] = request.POST['email']
                return redirect('home')
            else: 
                return render(request, 'login.html', {'msg': 'Invalid password'})
        except:
            return render(request, 'login.html', {'msg': 'Email does not exist!!'})
    
def logout(request):
    try:
        del request.session['user_email']
        global user_obj
        del user_obj
        return render (request, 'index.html', {'home': 'active'})
    except:
        return redirect ('login')

def add_blog(request):
    if request.method == 'GET':
        try:
            return render(request, 'add_blog.html', {'userdata': user_obj} )
        except:
            return redirect('login')
    else:
        Blog.objects.create(
            title = request.POST['title'],
            desc = request.POST['description'],
            categories = request.POST['category'],
            picture = request.FILES['photo'],
            user = user_obj
        )
        return redirect('home')
    
def my_blogs(request):
    my_filtered_blogs = Blog.objects.filter(user = user_obj)
    return render(request, 'my_blogs.html', {'my_blogs': 'active', 'userdata': user_obj, 'blogs': my_filtered_blogs})

def singleblog(request, pk):
    single_blog = Blog.objects.get(id = pk)
    my_filtered_comments = Comments.objects.filter(blog = single_blog)
    donate_list = Donation.objects.filter(pay_to = single_blog)
    donate_amount = 0
    global amount
    for i in donate_list:
        donate_amount += i.amount
        print(i.amount)
    try:
        return render(request, 'singleblog.html',{'blog': single_blog, 'userdata': user_obj, 'all_comments':my_filtered_comments, 'donations' : donate_amount})
    except:
        return render(request, 'singleblog.html',{'blog': single_blog, 'all_comments':my_filtered_comments, 'donations' : donate_amount}) 

def add_comment(request, blog_id):
    # blog_id = kaya blog par comment aai te
    try:
        user_obj = User.objects.get(email = request.session['user_email'])
        blog_obj = Blog.objects.get(id = blog_id)
        Comments.objects.create(
            message = request.POST['comment_msg'],
            blog = blog_obj,
            user = user_obj
        )
        my_filtered_comments = Comments.objects.filter(blog = blog_obj)
        return render(request, 'singleblog.html', {'blog':blog_obj, 'userdata': user_obj, 'all_comments':my_filtered_comments})
    except:
        return redirect('login')

def searched_blog(request):
    search_words = request.POST['search']
    filtered_blogs = Blog.objects.filter(title__icontains = search_words)
    return render(request, 'searched_blog.html', {'blogs': filtered_blogs})
    
def donate(request, blog_id):
    try:    
        user_obj = User.objects.get(email = request.session['user_email'])
        global blog_obj
        blog_obj = Blog.objects.get(id = blog_id)
        if request.method == "POST":

        # --------- copied code(fun 1) from razorpay inter=gration in django ----------- #
            currency = 'INR'
            global amount
            amount = int(request.POST['donate_amount']) * 100
    
            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'
        
            # we need to pass these details to frontend.
            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
            return render(request, 'razorpay_chaiwala_page.html', context=context)
        else:
            return render(request, 'donate.html', {'blog':blog_obj, 'userdata': user_obj})
    except:
        return redirect('login')

# --------- copied code(fun 2) from razorpay inter=gration in django ----------- #

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        user_obj = User.objects.get(email = request.session['user_email'])
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount) 
                    # render success page on successful caputre of payment
                    Donation.objects.create(
                        pay_by = user_obj,
                        pay_to = blog_obj,
                        amount = amount/100 #1000/100 = 10 inr
                    )
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

def my_profile(request):
    if request.method == 'GET':
        try:
            user_obj = User.objects.get(email = request.session['user_email'])
            return render(request, 'my_profile.html', {'userdata': user_obj})
        except:
            return redirect('login')
    else:
        user_obj = User.objects.get(email = request.session['user_email'])
        user_obj.first_name = request.POST['first_name']
        user_obj.last_name = request.POST['last_name']
        user_obj.username = request.POST['username']
        user_obj.save()
        return render(request, 'my_profile.html', {'userdata':user_obj, 'msg': 'Updated!!'})