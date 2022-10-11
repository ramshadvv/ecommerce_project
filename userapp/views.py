from datetime import datetime
import json
import re
from django.shortcuts import render, redirect
from accounts.models import Accounts, CustomerAdress
from adminapp.models import Trial
from django.contrib.auth import authenticate
from django.contrib import messages
from cartapp.models import CartItem, Order, MyWishList
from productapp.models import Category, Coupen, Product
from django.db.models import Q
import os
from decouple import config
from twilio.rest import Client
import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt


number=''


# Create your views here.


def home(request):
    if 'user_id' in request.session:
        if 'search' in request.GET:
            sh          = request.GET['search']
            multiple_sh = Q(Q(product_name__icontains=sh) | Q(brand__icontains=sh))
            item        = Product.objects.filter(multiple_sh).order_by("id")
            searched    = True
            user        = Accounts.object.get(username = request.session['user_id'])
            wish        = MyWishList.objects.filter(username = user.id)
            wishlist    = []
            for i in wish:
                wishlist.append(i.product.product_name)
            context     = {
                'data':item,
                'searched':searched,
                'wishlist':wishlist
            }
        else:
            item      = Product.objects.all().order_by("id")
            user      = Accounts.object.get(username = request.session['user_id'])
            wish      = MyWishList.objects.filter(username = user.id)
            wishlist  = []
            for i in wish:
                wishlist.append(i.product.product_name)
            context = {
                'data':item,
                'wishlist':wishlist
            }
    else:
        if 'search' in request.GET:
            sh          = request.GET['search']
            multiple_sh = Q(Q(product_name__icontains=sh) | Q(brand__icontains=sh))
            item        = Product.objects.filter(multiple_sh).order_by("id")
            searched    = True
            wishlist  = []
            context     = {
                'data':item,
                'searched':searched,
                'wishlist':wishlist
            }
        else:
            item    = Product.objects.all().order_by("id")
            wishlist  = []
            context = {
                'data':item,
                'wishlist':wishlist
            }
    return render(request, 'user/index.html',context)


def sortwithprice(request, value, category):
    wishlist  = []
    selected = None
    if Category.objects.filter(category_name=category) and value == 'hightolow':
        category = Category.objects.get(category_name = category)
        selected = category.category_name
        item     = Product.objects.filter(category = category.id).order_by("-price")
        if 'user_id' in request.session:
            user      = Accounts.object.get(username = request.session['user_id'])
            wish      = MyWishList.objects.filter(username = user.id)
            for i in wish:
                wishlist.append(i.product.product_name)
            print(wishlist)
    elif Category.objects.filter(category_name=category) and value == 'lowtohigh':
        category = Category.objects.get(category_name = category)
        selected = category.category_name
        item     = Product.objects.filter(category = category.id).order_by("price")
        if 'user_id' in request.session:
            user      = Accounts.object.get(username = request.session['user_id'])
            wish      = MyWishList.objects.filter(username = user.id)
            for i in wish:
                wishlist.append(i.product.product_name)
            print(wishlist)
    elif value == 'hightolow':
        item     = Product.objects.all().order_by("-price")
        if 'user_id' in request.session:
            user      = Accounts.object.get(username = request.session['user_id'])
            wish      = MyWishList.objects.filter(username = user.id)
            for i in wish:
                wishlist.append(i.product.product_name)
            print(wishlist)
    else:
        item     = Product.objects.all().order_by("price")
        if 'user_id' in request.session:
            user      = Accounts.object.get(username = request.session['user_id'])
            wish      = MyWishList.objects.filter(username = user.id)
            for i in wish:
                wishlist.append(i.product.product_name)
            print(wishlist)
    print(wishlist)
    context = {
        'data':item,
        'selected':selected,
        'wishlist':wishlist
    }
    return render(request, 'user/index.html',context)


def selectedView(request,value):
    category = Category.objects.get(category_name = value)
    selected = category.category_name
    item     = Product.objects.filter(category = category.id).order_by("id")
    category = Category.objects.all()
    wishlist = []
    if 'user_id' in request.session:
        user      = Accounts.object.get(username = request.session['user_id'])
        wish      = MyWishList.objects.filter(username = user.id)
        for i in wish:
            wishlist.append(i.product.product_name)
        print(wishlist)
    context  = {
        'data':item,
        'category':category,
        'selected':selected,
        'wishlist':wishlist
    }
    return render(request, 'user/index.html',context)


def product_details(request,id):
    item = Product.objects.get(id = id)
    return render(request, 'user/productdetails.html',{'thisProduct':item})


def user_login(request):
    if 'user_id' in request.session:
        return redirect(home)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        if username == '' and password == '':
            messages.error(request, 'Please enter the values!!!')
            return redirect(user_login)
        elif Accounts.objects.filter(username = username):
            data = Accounts.objects.get(username = username)
            if data.is_active == False :
                messages.error(request, 'Your account got blocked!!!')
                return redirect(user_login)
            user = authenticate(username = username, password = password)
            if user is not None and data.username != 'admin':
                request.session['user_id'] = username
                session_key = request.session.session_key
                if Order.objects.filter(guest_user = session_key, orderd = False):
                    order_guest_qs = Order.objects.filter(guest_user = session_key, orderd = False)
                    order_guest_qs = order_guest_qs[0]
                    item           = Accounts.object.get(username = username)
                    id             = item.id
                    order_qs       = Order.objects.filter(user_id= id, orderd = False)
                    if order_qs.exists():
                        order = order_qs[0]
                        if order.items.filter(user_id=id).exists():
                            order_item = order.items.filter(user_id=id)
                            order_item = order_item[0]
                            for i in order_guest_qs.items.all():
                                product_item = Product.objects.get(product_name = i.product)
                                product_id   = product_item.id
                                if order.items.filter(product_id = product_id).exists():
                                    order_cart_item =order.items.get(user_id=id,product=product_id)
                                    print(order_cart_item.quantity)
                                    # order_cart_item = CartItem.objects.get(user_id=id,product=product_id)
                                    order_cart_item.quantity += int(i.quantity)
                                    print(order_cart_item.quantity)
                                    order_cart_item.save()
                                    order.save()
                                    i.delete()
                                else:
                                    order_cart_item            = CartItem.objects.create(user_id=id)
                                    order_cart_item.product    = Product.objects.get(product_name = i.product)
                                    order_cart_item.quantity   = i.quantity
                                    order_cart_item.guest_user = ''
                                    order_cart_item.save()
                                    order.items.add(order_cart_item)
                                    order.save()
                                    i.delete()
                            order_guest_qs.delete()
                            return redirect(home)
                        else:
                            for i in order_guest_qs.items.all():
                                order_item            = CartItem.objects.create(user_id=id)
                                order_item.product    = Product.objects.get(product_name = i.product)
                                order_item.quantity   = i.quantity
                                order_item.guest_user = ''
                                order_item.save()
                                order.items.add(order_item)
                                order.save()
                                i.delete()
                            order_guest_qs.delete()
                            return redirect(home)
                    else:
                        order = Order.objects.create(user_id = id)
                        for i in order_guest_qs.items.all():
                            order_item            = CartItem.objects.create(user_id=id)
                            order_item.product    = Product.objects.get(product_name = i.product)
                            order_item.quantity   = i.quantity
                            order_item.guest_user = ''
                            order_item.save()
                            order.items.add(order_item)
                            order.save()
                        order_guest_qs.delete()
                        return redirect(home)
                else:
                    return redirect(home)

            else:
               messages.error(request, 'Invalid Credentials!!!')
               return redirect(user_login)
        else:
            messages.error(request, 'User is not exists!!!')
            return redirect(user_login)
    return render(request, 'user/login.html')


def passwordverification(request):
    if request.method == 'POST':
        number = request.POST['number']
        if number == '' or len(number) != 10 :
            messages.error(request, 'Please enter valid phone number!!!')
            return redirect(passwordverification)
        elif Accounts.object.filter(phone = number):
            context = {
                'number':number
            }
            number = "+91" + number
            SendOTP(number)
            return render(request, 'user/passwordverification.html', context)
        else: 
            messages.error(request, 'Phone number is not registerd!!!')
            return redirect(signup)
    context = {
        'passwordverify':True
    }
    return render(request, 'user/otp_login.html', context)


def otpverificationpassword(request):
    if request.method  == 'POST':
        number          = request.POST['phone']
        otp_pattern     = "^[0-9\s]{3,}$"
        otp             = request.POST['number']
        username_verify = re.match(otp_pattern,otp)
        if len(otp)!=6 or request.POST ['number'] == '':
            messages.error(request,'Invalid OTP ', extra_tags='errorotp') 
            return render(request, 'user/passwordverification.html',{'number':number})
        elif username_verify is None:
            messages.error(request,'Invalid OTP', extra_tags='errorotp') 
            return render(request, 'user/passwordverification.html',{'number':number})
        if Accounts.object.filter(phone = number):
            user   = Accounts.objects.get(phone = number)
            number = '+91'+ user.phone
            if check(otp,number):
                context={
                    'user' : user
                }
                return render(request, 'user/resetpassword.html', context)
            else:
                messages.error(request,'Invalid OTP ', extra_tags='errorotp') 
                return redirect(otpverificationpassword)
        else:
            messages.error(request,'You are not registerd!!') 
            return redirect(signup)
    return render(request, 'user/passwordverification.html')


def resetpassword(request):
    if request.method == 'POST':
        username = request.POST['username']
        npass    = request.POST['pass']
        npass1   = request.POST['pass1']
        if Accounts.object.filter(username=username):
            item  = Accounts.objects.get(username=username)
            if username=='' or npass=='' or npass1 == '':
                messages.error(request,'All fields are required')
                context = {
                    'user':item
                }
                return render(request, 'user/resetpassword.html', context)
            elif len(npass)<8:
                messages.error(request,'Password atleast 8 charecters')
                context = {
                    'user':item
                }
                return render(request, 'user/resetpassword.html', context)
            elif npass != npass1:
                messages.error(request,'Password is not match') 
                context = {
                    'user':item
                }
                return render(request, 'user/resetpassword.html', context)
            else:
                    print('success')
                    item.set_password(npass)
                    print(item.set_password(npass))
                    item.save()
                    return redirect(user_login)
        else:
            messages.error(request,'User is not Exists') 
            return redirect(signup)
    return redirect(user_login)


def otp_login(request):
    if request.method == 'POST':
        if request.POST['number'] == '':
            messages.error(request, 'Please enter valid phone number!!!')
            return redirect(otp_login)
        num = request.POST['number']
        if len(num) != 10:
                messages.error(request, 'Please enter valid phone number!!!')
                return redirect(otp_login)
        if Accounts.object.filter(phone = num):
            number = "+91" + num
            SendOTP(number)
            context = {
                'number':num
            }
            return render(request, 'user/otpphonelogin.html', context)
        else: 
            messages.error(request, 'Phone number is not registerd!!!')
            return redirect(signup)
    else:
        return render(request, 'user/otp_login.html')


def signup(request):
    if request.method == 'POST':
        username     = request.POST['username']
        first_name   = request.POST['first_name']
        last_name    = request.POST['last_name']
        email        = request.POST['email']
        phone_number = request.POST['phone_number']
        password     = request.POST['pass']
        password1    = request.POST['pass1']

        if password == password1 and len(password)>=6:
            try:
                k=int(request.POST['phone_number'])
            except:
                messages.error(request,'Please enter the phone Number',extra_tags='signphone_number')
                return redirect(signup)
            if username == '' or email == '' or phone_number == '' or password == '' or password1 == '':
                messages.error(request, 'Username must not be empty', extra_tags='signusername')
                messages.error(request, 'Email must not be empty', extra_tags='signemail')
                messages.error(request, 'Password must not be empty', extra_tags='signpass')
                messages.error(request, 'Phone number must not be empty', extra_tags='signphone_number')
                return redirect(signup)
            elif len(phone_number)!=10:
                messages.error(request, 'Enter corrrect phone number', extra_tags='signphone_number')
                return redirect(signup)
            elif Accounts.object.filter(username=username):
                messages.error(request, 'username already  exists', extra_tags='signusername')
                return redirect(signup)
            elif Accounts.object.filter(email=email):
                messages.error(request, 'Email already  exists', extra_tags='signemail')
                return redirect(signup)
            elif Accounts.object.filter(phone=phone_number):
                messages.error(request, 'Phone number already  exists', extra_tags='signphone_number')
                return redirect(signup)
            else:
                if Trial.objects.filter(username=username):
                    messages.error(request, 'Username already exists', extra_tags='signusername')
                    return redirect(signup)
                else:
                    item = Trial.objects.create(
                        username = username, 
                        first_name = first_name, 
                        last_name=last_name, 
                        email=email,
                        phone = phone_number,
                        password = password
                    )
                    request.session['user_id'] = username
                    number = "+91" + phone_number
                    if SendOTP(number):
                        item.save()
                    return render(request, 'user/otp.html')  
        else:
            messages.error(request, '''Password must be same 
            and must have 6 charecters''', extra_tags='signpass')
            return redirect(signup)
    return render(request, 'user/signup.html')


def profileedit(request):
    if 'user_id' in request.session:
        user = request.session.get('user_id')
        item = Accounts.object.get(username=user)
        if request.method == 'POST':
            username     = request.POST['username']
            first_name   = request.POST['first_name']
            last_name    = request.POST['last_name']
            email        = request.POST['email']
            phone_number = request.POST['phone_number']
            try:
                k=int(request.POST['phone_number'])
            except:
                messages.error(request,'Please enter the phone Number',extra_tags='signphone_number')
                return redirect(profileedit)
            if username == '' or email == '' or phone_number == '':
                messages.error(request, 'Username must not be empty', extra_tags='signusername')
                messages.error(request, 'Email must not be empty', extra_tags='signemail')
                messages.error(request, 'Phone number must not be empty', extra_tags='signphone_number')
                return redirect(profileedit)
            elif len(phone_number)!=10:
                messages.error(request, 'Enter corrrect phone number', extra_tags='signphone_number')
                return redirect(profileedit)
            elif Accounts.object.filter(username=username) and username != user:
                messages.error(request, 'username already  exists', extra_tags='signusername')
                return redirect(profileedit)
            elif Accounts.object.filter(email=email) and username != user:
                messages.error(request, 'Email already  exists', extra_tags='signemail')
                return redirect(profileedit)
            elif Accounts.object.filter(phone=phone_number) and username != user:
                messages.error(request, 'Phone number already  exists', extra_tags='signphone_number')
                return redirect(profileedit)
            else:
                item.username   = username
                item.first_name = first_name
                item.last_name  = last_name
                item.email      = email
                item.phone      = phone_number
                item.save()
                return redirect(profile)
        else:
            return render(request, 'user/profileedit.html', {'data' : item})


def addaddress(request):
    if request.method == 'POST':
        user         = request.session.get('user_id')
        first_name   = request.POST['first_name']
        last_name    = request.POST['last_name']
        email        = request.POST['email']
        phone_number = request.POST['phone_number']
        house_name   = request.POST['house_name']
        street_name  = request.POST['street_name']
        city         = request.POST['city']
        state        = "Kerala"
        country      = "India"
        post_code    = request.POST['post_code']
        item = CustomerAdress.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            house_name=house_name,
            street_name=street_name,
            city=city,
            state=state,
            country=country,
            post_code=post_code
        )
        item.user = Accounts.object.get(username = user)
        item.save()
        return redirect(profile)
    return render(request, 'user/addaddress.html')


def edit_address(request, id):
    item = CustomerAdress.objects.get(id = id)
    if request.method == 'POST':
        item.first_name   = request.POST['first_name']
        item.last_name    = request.POST['last_name']
        item.email        = request.POST['email']
        item.phone_number = request.POST['phone_number']
        item.house_name   = request.POST['house_name']
        item.street_name  = request.POST['street_name']
        item.city         = request.POST['city']
        item.state        = "Kerala"
        item.country      = "India"
        item.post_code    = request.POST['post_code']
        item.save()
        return redirect(profile)
    context = {
        'item': item
    }
    return render(request, 'user/addressedit.html', context)


def delete_address(request, id):
    item = CustomerAdress.objects.get(id = id)
    item.delete()
    return redirect(profile)


def otp_verification_phone(request):
    if request.method  == 'POST':
        number          = request.POST ['phone']
        otp_pattern     = "^[0-9\s]{3,}$"
        otp             = request.POST ['number']
        username_verify = re.match(otp_pattern,otp)
        if len(otp)!=6 or request.POST ['number'] == '':
            messages.error(request,'Invalid OTP ', extra_tags='errorotp') 
            return redirect(otp_verification_phone)
        elif username_verify is None:
            messages.error(request,'Invalid OTP', extra_tags='errorotp') 
            return redirect(otp_verification_phone)
        if Accounts.object.filter(phone = number):
            user   = Accounts.objects.get(phone = number)
            number = '+91'+ user.phone
            if check(otp,number):
                request.session['user_id'] = user.username
                session_key = request.session.session_key
                if Order.objects.filter(guest_user = session_key):
                    order_guest_qs = Order.objects.get(guest_user = session_key)
                    item           = Accounts.object.get(username = user.username)
                    id             = item.id
                    order_qs       = Order.objects.filter(user_id= id, orderd = False)
                    if order_qs.exists():
                        order = order_qs[0]
                        if order.items.filter(user_id=id).exists():
                            order_item = order.items.filter(user_id=id)
                            order_item = order_item[0]
                            for i in order_guest_qs.items.all():
                                product_item = Product.objects.get(product_name = i.product)
                                product_id   = product_item.id
                                if order.items.filter(product_id = product_id).exists():
                                    order_cart_item =order.items.get(user_id=id,product=product_id)
                                    print(order_cart_item.quantity)
                                    # order_cart_item = CartItem.objects.get(user_id=id,product=product_id)
                                    order_cart_item.quantity += int(i.quantity)
                                    print(order_cart_item.quantity)
                                    order_cart_item.save()
                                    order.save()
                                    i.delete()
                                else:
                                    order_cart_item            = CartItem.objects.create(user_id=id)
                                    order_cart_item.product    = Product.objects.get(product_name = i.product)
                                    order_cart_item.quantity   = i.quantity
                                    order_cart_item.guest_user = ''
                                    order_cart_item.save()
                                    order.items.add(order_cart_item)
                                    order.save()
                                    i.delete()
                            order_guest_qs.delete()
                            return redirect(home)
                        else:
                            for i in order_guest_qs.items.all():
                                order_item            = CartItem.objects.create(user_id=id)
                                order_item.product    = Product.objects.get(product_name = i.product)
                                order_item.quantity   = i.quantity
                                order_item.guest_user = ''
                                order_item.save()
                                order.items.add(order_item)
                                order.save()
                                i.delete()
                            order_guest_qs.delete()
                            return redirect(home)
                    else:
                        order = Order.objects.create(user_id = id)
                        for i in order_guest_qs.items.all():
                            order_item            = CartItem.objects.create(user_id=id)
                            order_item.product    = Product.objects.get(product_name = i.product)
                            order_item.quantity   = i.quantity
                            order_item.guest_user = ''
                            order_item.save()
                            order.items.add(order_item)
                            order.save()
                        order_guest_qs.delete()
                        return redirect(home)
                else:
                    return redirect(home)
            else:
                messages.error(request,'Invalid OTP ', extra_tags='errorotp') 
                return redirect(otp_verification_phone)
        else:
            messages.error(request,'You are not registerd!!') 
            return redirect(signup)
    return render(request, 'user/otpphonelogin.html')


def otp_verification(request):
    if request.session.get('user_id'):
        user = request.session.get('user_id')
        user = Trial.objects.filter(username = user)
        for i in user: 
            num = i.phone
        number = '+91'+num
        if request.method  == 'POST':
            otp_pattern     = "^[0-9\s]{3,}$"
            otp             = request.POST ['number']
            username_verify = re.match(otp_pattern,otp)
            if len(otp)!=6 or request.POST ['number'] == '':
                messages.error(request,'Invalid OTP ', extra_tags='errorotp') 
                return redirect(otp_verification)
            elif username_verify is None:
                messages.error(request,'Invalid OTP', extra_tags='errorotp') 
                return redirect(otp_verification)
            else:
                if check(otp,number):
                    for i in user:
                        item = Accounts.objects.create(
                            username = i.username, 
                            first_name = i.first_name, 
                            last_name=i.last_name, 
                            email=i.email,
                            phone = i.phone
                        )
                        item.set_password(i.password)
                        item.save()
                    user.delete()
                    return redirect(home)
                else:
                    messages.error(request,'Invalid OTP ', extra_tags='errorotp') 
                    return redirect(otp_verification)
    return render(request, 'user/otp.html')


def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        return redirect(home)
    return render(request,'user/login.html')


def SendOTP(num):
    global number 
    number      = num
   
    account_sid = os.environ['TWILIO_ACCOUNT_SID'] =config('ACCOUNT_SID')
    
    auth_token  = os.environ['TWILIO_AUTH_TOKEN'] = config('AUTH_TOKEN')
 
    client      = Client(account_sid, auth_token)
    
    verification = client.verify \
        .services(config('services')) \
        .verifications.create(to=number, channel='sms')
    print(verification.status)
    
    return True


def check(otp,number):
    account_sid = os.environ['TWILIO_ACCOUNT_SID'] =config('ACCOUNT_SID')
    auth_token  = os.environ['TWILIO_AUTH_TOKEN'] =config('AUTH_TOKEN')
    client      = Client(account_sid, auth_token)

    verification_check = client.verify \
                            .services(config('services')) \
                            .verification_checks.create(to=number, code=otp)
    print(verification_check.status)
    print(verification_check)

    if verification_check.status ==  'approved':
        return True
    else:
        return False


def wishlistview(request):
    if 'user_id' in request.session:
        user    = Accounts.object.get(username = request.session.get('user_id'))
        item    = MyWishList.objects.filter(username=user.id)
        context = {
            'data':item
        }
        return render(request, 'user/wishlist.html', context)
    else:
        messages.error(request, 'Login is required')
        return redirect(user_login)


def wishlistadd(request, id):
    if 'user_id' in request.session:
        user     = request.session.get('user_id')
        user     = Accounts.object.get(username = user)
        product  = Product.objects.get(id = id)
        if MyWishList.objects.filter(username_id = user.id,product_id = product.id):
            return redirect(home)
        if MyWishList.objects.filter(id=product.id).exists():
            return redirect(home)
        else:
            item = MyWishList.objects.create(username_id = user.id,product_id = product.id )
            return redirect(home)
    else:
        messages.error(request, 'Login is required')
        return redirect(user_login)


def wishlistitemdelete(request, id):
    item = MyWishList.objects.get(id=id)
    item.delete()
    return redirect(wishlistview)


def wishlistdelete(request, id):
    if 'user_id' in request.session:
        user     = request.session.get('user_id')
        user     = Accounts.object.get(username = user)
        item     = MyWishList.objects.get(username= user.id,product=id)
        item.delete()
        return redirect(home)
    else:
        messages.error(request, 'Login is required')
        return redirect(user_login)
        

def cartview(request):
    if 'user_id' in request.session:
        user     = request.session.get('user_id')
        order_qs = Order.objects.filter(user__username = user, orderd=False).order_by('date_ordered')
        cart_qs  = CartItem.objects.filter(user__username = user)
        if order_qs.exists() and cart_qs.exists():
            order_object = order_qs[0]
        else:
            return render(request,'user/cartempty.html')
        context = {
            'order_object' : order_object
        }
    else:
        user     = request.session.session_key
        order_qs = Order.objects.filter(guest_user = user, orderd=False).order_by('date_ordered')
        cart_qs  = CartItem.objects.filter(guest_user = user)
        if order_qs.exists() and cart_qs.exists():
            order_object = order_qs[0]
        else:
            return render(request,'user/cartempty.html')
        context = {
            'order_object' : order_object
        }
    return render(request,'user/cart.html', context)


def cartadd(request):
    if 'user_id' in request.session:
        if request.method== 'POST':
            product_id  = request.POST.get('product-id')
            quantity    = int(request.POST.get('product-quantity'))
            product_var = Product.objects.get(id=product_id)
            user        = request.session.get('user_id')
            item        = Accounts.object.get(username = user)
            id          = item.id
            order_qs= Order.objects.filter(user_id= id, orderd = False)
            if order_qs.exists():
                order = order_qs[0]
                if order.items.filter( user_id=id, product=product_var).exists():
                    order_item           = order.items.get( user_id=id, product=product_var)
                    order_item.quantity += quantity
                    order_item.save()
                    try:
                        wishlist_item = MyWishList.objects.get(username=id, product = product_id)
                        wishlist_item.delete()
                    except:
                        pass
                    return redirect('/product/'+str(product_id))
                else:
                    order_item = CartItem.objects.create(user_id=id, product = product_var, quantity=quantity)
                    order.items.add(order_item)
                    order.save()
                    try:
                        wishlist_item = MyWishList.objects.get(username=id, product = product_id)
                        wishlist_item.delete()
                    except:
                        pass
                    return redirect('/product/'+str(product_id))
            else:
                order      = Order.objects.create(user_id=id)
                order_item = CartItem.objects.create(user_id=id, product=product_var, quantity=quantity)
                order.items.add(order_item)
                order.save()
                try:
                    wishlist_item = MyWishList.objects.get(username=id, product = product_id)
                    wishlist_item.delete()
                except:
                    pass
                return redirect('/product/'+str(product_id))
    else:
        product_id  = request.POST.get('product-id')
        quantity    = int(request.POST.get('product-quantity'))
        product_var = Product.objects.get(id=product_id)
        id          = request.session.session_key
        order_qs= Order.objects.filter(guest_user= id, orderd = False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter( guest_user=id, product=product_var).exists():
                order_item           = order.items.get( guest_user=id, product=product_var)
                order_item.quantity += quantity
                order_item.save()
                try:
                    wishlist_item = MyWishList.objects.get(username=id, product = product_id)
                    wishlist_item.delete()
                except:
                    pass
                return redirect('/product/'+str(product_id))
            else:
                order_item = CartItem.objects.create(guest_user=id, product = product_var, quantity=quantity)
                order.items.add(order_item)
                order.save()
                try:
                    wishlist_item = MyWishList.objects.get(username=id, product = product_id)
                    wishlist_item.delete()
                except:
                    pass
                return redirect('/product/'+str(product_id))
        else:
            order      = Order.objects.create(guest_user=id)
            order_item = CartItem.objects.create(guest_user=id, product=product_var, quantity=quantity)
            order.items.add(order_item)
            order.save()
            try:
                wishlist_item = MyWishList.objects.get(username=id, product = product_id)
                wishlist_item.delete()
            except:
                pass
            return redirect('/product/'+str(product_id))


def deleteFromCart(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect(cartview)
        

@csrf_exempt
def changeQuantity(request):
    data  = json.loads(request.body)
    count = int(data['count'])
    id    = data['cart']
    item  = CartItem.objects.get(id=id)
    if item.quantity == 1 and count == -1:
        return redirect(cartview)
    if count == 1:
        item.quantity += 1
    else:
        item.quantity -= 1
    item.save()
    return JsonResponse('success', safe = False) 


def checkoutview(request):
    if 'user_id' in request.session:
        user     = request.session['user_id']
        user_id  = Accounts.object.get(username = user)
        addresses = None
        if CustomerAdress.objects.filter(user = user_id):
            addresses = CustomerAdress.objects.filter(user = user_id) 
            addresses = addresses[0] 
        order_qs = Order.objects.filter(user__username=user, orderd=False)
        cart_qs  = CartItem.objects.filter(user = user_id.id)
        add_qs   = CustomerAdress.objects.filter(user__username=user)
        payment  = 0
        offer    = 0
        discount = 0
        if order_qs.exists():
            order = order_qs[0]
        else:
            order= Order.objects.create(user_id=user_id.id)
        

        if order_qs.exists():
            orders       = order_qs[0]
            total_amount = float(orders.total_amount_cart)
            tax          = (total_amount) * 3 /100
            coupen_check = False
            coupen_code  = None
            if request.method == 'POST':
                if Coupen.objects.filter(coupencode = request.POST['coupen'], is_active=True) and Order.objects.filter(orderd=False):
                    coupen_code    = request.POST['coupen']
                    current_total  = request.POST['current_total']
                    
                    coupen_qs      = Coupen.objects.get(coupencode = coupen_code)
                    found          = False
                    for i in coupen_qs.users.all():
                        if str(i.username) == str(user):
                            found = True
                            break
                    if found == False :
                        if coupen_qs.expiry_date < datetime.now().date():
                            coupen_qs.is_active = False
                            coupen_qs.save()
                            messages.error(request, 'Coupen is not available',extra_tags='coupenerror')
                        else:
                            total_amount -= ((total_amount * coupen_qs.coupen_offer)/100)
                            total_amount  = "{:.1f}".format(total_amount)
                            coupen_check  = True
                            offer         = coupen_qs.coupen_offer
                            discount      = float(current_total) - float(total_amount)
                            discount      = "{:.1f}".format(discount)
                            discount      = float(discount)
                    else:
                        messages.error(request, 'Coupen is already used',extra_tags='coupenerror')
                    
                else:
                    messages.error(request, 'Coupen is not available',extra_tags='coupenerror')
            grand_total = float(total_amount) + float(tax)
            grand_total = "{:.1f}".format(grand_total)
            grand_total = float(grand_total)
        else:
            messages.error(request, 'Please add an product',extra_tags='ordererror')
            return redirect(cartview)
        try:
            key = config("KEY_ID")
            secret_key = config("KEY_SECRET")
            client = razorpay.Client(
                auth=(key,secret_key))
            currency = 'INR'
            payment  = client.order.create({'amount':10 * 100, 'currency':currency, 'payment_capture': '1'})
        except:
            print("Razorpay error")
        usd_amount = grand_total / 76
        usd_amount = "{:.2f}".format(usd_amount)
        context    = {
            'order' : order,
            'add_qs':add_qs,
            'key':key,
            'payment':payment,
            'cart':cart_qs,
            'coupen_code':coupen_code,
            'grand_total' :grand_total,
            'coupen_check':coupen_check,
            'offer':offer,
            'discount':discount,
            'usd_amount':usd_amount,
            'addresses':addresses
        }
        return render(request, 'user/checkout.html',context)
    else:
        messages.error(request, 'Login is required')
        return redirect(user_login)


@csrf_protect
def order_placingView(request):
    if request.session.get('user_id'):
        data           = json.loads(request.body)
        payment_method = data['payment']
        address_id     = data['address']
        get_total      = data['get_total']
        discount       = data['discount']
        user           = request.session['user_id']
        order_qs       = Order.objects.filter(user__username=user, orderd=False)
        user_id        = Accounts.object.get(username = user)
        coupen_check   = data['coupen_check']
        coupen_code    = data['coupen_code']
        if coupen_check == 'True':
            coupen = Coupen.objects.get(coupencode = coupen_code)
            coupen.users.add(user_id.id)
            print('coupenapplied')
            coupen.save()
        if order_qs.exists():
            order                = order_qs[0]
            order.Customer       = CustomerAdress.objects.get(id = address_id)
            order.payment_method = payment_method
            order.discount       = discount
            order.total_price    = get_total
            order.orderd         = True
            order.save()
        return JsonResponse('cash on delivery', safe = False) 


def placed(request):
    if request.method == 'POST':
        user           = request.session['user_id']
        id             = request.POST.get('address_id')
        get_total      = request.POST.get('grand_total')
        discount       = request.POST.get('discount')
        payment_method = request.POST.get('payment')
        user_id        = Accounts.object.get(username = user)
        coupen_check   = request.POST.get('coupen_check')
        coupen_code    = request.POST.get('coupen_code')
        if coupen_check == 'True':
            coupen = Coupen.objects.get(coupencode = coupen_code)
            coupen.users.add(user_id.id)
            coupen.save()

        if payment_method == None or id == None:
            return redirect(checkoutview)
        order_qs = Order.objects.filter(user__username=user, orderd=False)
        if order_qs.exists():
            order                = order_qs[0]
            order.Customer       = CustomerAdress.objects.get(id = id)
            order.payment_method = payment_method
            order.total_price    = get_total
            order.discount       = discount
            order.orderd         = True
            order.save()
            return render(request, 'user/placeorder.html')
        else:
            order                = Order.objects.create(user__username=user)
            order.Customer       = CustomerAdress.objects.get(id = id)
            order.payment_method = payment_method
            order.total_price    = get_total
            order.discount       = discount
            order.orderd         = True
            order.save()
            return render(request, 'user/placeorder.html')
    else:
        return render(request, 'user/placeorder.html')


def profile(request):
    if 'user_id' in request.session:
        user      = request.session['user_id']
        user_id   = Accounts.object.get(username = user)
        addresses = CustomerAdress.objects.filter(user = user_id)
        context   = {
            'addresses' : addresses
        }
    return render(request, 'user/profile.html', context)
    
def myorders(request):
    user     = request.session['user_id'] 
    order_qs = Order.objects.filter(user__username=user, orderd=True)
    for i in order_qs:
        if i.status == 'Delivered' and i.returnexpiry == True:
            try:
                age = datetime.now().date()-i.date_delivered
                k   = str(age)
                k   = k.split()
                age = int(k[0])
                if age > 7 :
                    i.returnexpiry = False
                    i.save()
            except:
                pass
        else:
            pass
    if order_qs.exists():
        context = {
        'order' : order_qs
    }
    else:
        return render(request,'user/orderempty.html')
    return render(request, 'user/order.html', context)


def cancelFromOrder(request, item_id, order_id):
    if request.method == 'GET':
        reason             = request.GET['reason']
        order              = Order.objects.get(id=order_id)
        item               = CartItem.objects.get(id=item_id)
        item.cancel_status = True
        item.reason        = reason
        item.save()
        flag = 1
        for i in order.items.all():
            if i.cancel_status != True:
                flag = -1
                break
        
        if flag == 1:
            order.status = "Canceled"
            order.date_delivered = datetime.now().date()
        order.total_price -= item.product.price
        order.save()
        return redirect(myorders)
    else:
        return redirect(myorders)


def return_status_view(request,id):
    if request.method == 'GET':
        reason                       = request.GET['reason']
        return_status                = Order.objects.get(id = id)        
        return_status.status         = "Returned"
        return_status.reason         = reason
        return_status.returnexpiry   = False
        return_status.date_delivered = datetime.now().date()
        for i in return_status.items.all():
            item        = Product.objects.get(id=i.product.id)
            item.stock += i.quantity
            item.save()
        return_status.save()

        return redirect(myorders)


def cancel_status_view(request,id):
        cancel_status                = Order.objects.get(id = id)
        cancel_status.status         = "Canceled"
        cancel_status.date_delivered = datetime.now().date()
        cancel_status.save()
        return redirect(myorders)


def razorpay_checkout(request):
    if request.session.get("user_id"):
        if request.method == 'GET':
            user           = request.session.get('user_id')
            payment        = request.GET['payment']
            get_total      =  request.GET['grandtotal']
            address        =  request.GET['address']
            discount       =  request.GET['discount']
            address        = CustomerAdress.objects.get(id = address)
            order_qs       = Order.objects.filter(user__username=user, orderd=False)
            user_id        = Accounts.object.get(username = user)
            coupen_check   = request.GET.get('coupen_check')
            coupen_code    = request.GET.get('coupen_code')
            if coupen_check == 'True':
                coupen = Coupen.objects.get(coupencode = coupen_code)
                coupen.users.add(user_id.id)
                coupen.save()
            if order_qs.exists():
                order                = order_qs[0]
                order.Customer       = CustomerAdress.objects.get(id = address.id)
                order.payment_method = payment
                order.total_price    = get_total
                order.discount       = discount
                order.orderd         = True
                order.save()
                return render(request, 'user/placeorder.html')
            else:
                order                = Order.objects.create(user__username=user)
                order.Customer       = CustomerAdress.objects.get(id = address.id)
                order.payment_method = payment
                order.total_price    = get_total
                order.discount       = discount
                order.orderd         = True
                order.save()
                return render(request, 'user/placeorder.html')
    else:
        messages.error(request, 'Login is required!!')
        return redirect(user_login)


def invoice(request, id):
    if 'user_id' in request.session:
        item    = Order.objects.get(id = id)
        invoice = True
        context = {
            'data':item,
            'invoice':invoice
        }
        return render(request, 'user/invoice.html',context)
    else:
        messages.error(request, 'Login is required!!')
        return redirect(user_login)


def test(request):
    items = CartItem.objects.all()
    for i in items:
        i.delete()
    return redirect(home)