from datetime import datetime

import xlwt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render

from accounts.models import Accounts
from cartapp.models import Order
from productapp.models import Category, Coupen, Product

# Create your views here.

def home(request):
    if 'admin_id' in request.session:
        customer_count  = product_count=category_count=order=total_earnings=order_count=cancel_order=delivered_order=active_user=inactive_user=0
        customer_count  = Accounts.objects.all().count() - 1
        product_count   = Product.objects.all().count()
        category_count  = Category.objects.all().count()
        order           = Order.objects.filter(orderd=True)
        year            = str(datetime.now().date())
        year            = year.split('-')
        total_earnings  = Order.objects.filter(orderd=True, status="Delivered", date_delivered__month = year[1])
        order_count     = order.count()
        cancel_order    = Order.objects.filter(status ='Canceled').count()  
        delivered_order = Order.objects.filter(status ='Delivered').count()
        active_user     = Accounts.objects.filter(is_active  = True).count() - 1
        inactive_user   = Accounts.objects.filter(is_active  =False ).count()
        month = Order.objects.aggregate(
            jan=Sum('total_price', filter = Q(date_ordered__month = 1, status ="Delivered", orderd = True)),
            feb=Sum('total_price', filter = Q(date_ordered__month = 2, status ="Delivered", orderd = True)),
            mar=Sum('total_price', filter = Q(date_ordered__month = 3, status ="Delivered", orderd = True)),
            apr=Sum('total_price', filter = Q(date_ordered__month = 4, status ="Delivered", orderd = True)),
            may=Sum('total_price', filter = Q(date_ordered__month = 5, status ="Delivered", orderd = True)),
            jun=Sum('total_price', filter = Q(date_ordered__month = 6, status ="Delivered", orderd = True)),
            jul=Sum('total_price', filter = Q(date_ordered__month = 7, status ="Delivered", orderd = True)),
            aug=Sum('total_price', filter = Q(date_ordered__month = 8, status ="Delivered", orderd = True)),
            sep=Sum('total_price', filter = Q(date_ordered__month = 9, status ="Delivered", orderd = True)),
            oct=Sum('total_price', filter = Q(date_ordered__month = 10, status ="Delivered", orderd = True)),
            nov=Sum('total_price', filter = Q(date_ordered__month = 11, status ="Delivered", orderd = True)),
            dec=Sum('total_price', filter = Q(date_ordered__month = 12, status ="Delivered", orderd = True)),
        )
        total_sum=0
        for i in total_earnings:
            if i.total_price != None:
                total_sum += i.total_price
        
        total_sum = "{:.2f}".format(total_sum)
        context = {
            'customer_count':customer_count,
            'product_count':product_count,
            'category_count':category_count,
            'order_count':order_count,
            'total_sum':total_sum,
            'cancel_order':cancel_order,
            'delivered_order':delivered_order,
            'active_user':active_user,
            'inactive_user':inactive_user,
            'month':month
        }
        return render(request, 'admin/admin_index.html', context)
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def products(request):
    if 'admin_id' in request.session:
        item = Product.objects.filter(product_status=True).order_by("id")
        return render(request, 'admin/products.html',{'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)


def product_add(request):
    if 'admin_id' in request.session:
        value = Category.objects.all()
        context = {
            'value' : value
        }
        if request.method == 'POST':
            product_name = request.POST['product_name']
            description = request.POST['description']
            price = request.POST['price']
            stock = request.POST['stock']
            category_name = request.POST['category']
            brand = request.POST['brand']
            image=image1=image2=''
            try:
                image = request.FILES['uploadFromPC']
                image1 = request.FILES['uploadFromPC1']
                image2 = request.FILES['uploadFromPC2']
            except:
                print('please add an image!!')

            print(price)
            
            if product_name == '' or description =='' or price=='' or stock==''or category_name == '' or brand=='' or image=='' or image1=='' or image2 == '':
                messages.error(request,'All fields are required', extra_tags='productadderror')
                return redirect(product_add)
            elif int(price)<0 or int(stock)<0:
                messages.error(request,'Negative number is not supportted for price and stock', extra_tags='productadderror')
                return redirect(product_add)
            elif category_name == 'Select One':
                messages.error(request,'Please select a category', extra_tags='productadderror')
                return redirect(product_add)
            
            if image == None:
                return redirect(product_add)
            product_status = request.POST['product_status']
            item = Product.objects.create(
                product_name=product_name,
                description=description,
                price=price,
                stock=stock,
                brand=brand,
                image=image,
                image1=image1,
                image2=image2,
                product_status=product_status
            )
            item.category = Category.objects.get(category_name=category_name)
            item.save()
            return redirect(products)
        return render(request, 'admin/productadd.html', context)
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)    
 

def product_edit(request, id):
    if 'admin_id' in request.session:
        item=Product.objects.get(id=id)
        value = Category.objects.all()
        print(request.FILES)
        if request.method == 'POST':
            product_name = request.POST['product_name']
            description = request.POST['description']
            price = request.POST['price']
            stock = request.POST['stock']
            category_name = request.POST['category']
            brand = request.POST['brand']
            try:
                image = request.FILES['uploadFromPC']
                image1 = request.FILES['uploadFromPC1']
                image2 = request.FILES['uploadFromPC2']
            except:
                print('please add an image!!')
            if product_name == '' or description =='' or price=='' or stock==''or category_name == '' or brand=='':
                messages.error(request,'All fields are required')
                return redirect('/admin/editproduct/'+str(id))
            elif int(price)<0 or int(stock)<0:
                messages.error(request,'Negative number is not supportted for price and stock', extra_tags='productadderror')
                return redirect('/admin/editproduct/'+str(id))
            elif category_name == 'Select One':
                messages.error(request,'Please select a category', extra_tags='productadderror')
                return redirect('/admin/editproduct/'+str(id))
            
            item.product_name = request.POST['product_name']
            item.description = request.POST['description']
            item.price = request.POST['price']
            item.stock = request.POST['stock']
            item.category.category_name = request.POST['category']
            item.brand = request.POST['brand']
            item.product_status = request.POST['product_status']
            try:       
                item.image = request.FILES['uploadFromPC']
                item.image1 = request.FILES['uploadFromPC1']
                item.image2 = request.FILES['uploadFromPC2']
            except:
                print('sdsdffdfdf')
            item.save()
            return redirect(products)
        return render(request, 'admin/productedit.html',{'data':item, 'value':value})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)


def product_delete(request, id):
    item=Product.objects.get(id=id)
    item.product_status = False
    item.stock = 0
    item.save()
    return redirect(products)


def offer_product(request):
    if 'admin_id' in request.session:
        item = Product.objects.all().order_by("id")
        return render(request, 'admin/productoffer.html',{'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def offer_product_add(request):
    products = Product.objects.all()
    if request.method == 'POST':
        if request.POST['product_offer'] == '' or len(request.POST['product_offer']) > 2 or int(request.POST['product_offer'])>70:
            messages.error(request,'Productoffer is not valid!! and must be below 70%', extra_tags='productadderror')
            return redirect(offer_product_add)
        elif request.POST['product_name'] == 'Select One':
            messages.error(request,'Please select a  product', extra_tags='productadderror')
            return redirect(offer_product_add)
        product            = request.POST['product_name']
        offer              = request.POST['product_offer']
        item               = Product.objects.get(product_name = product)
        item.product_offer = offer
        item.save()
        return redirect(offer_product)
    context = {
        'value':products
    }
    return render(request, 'admin/productofferadd.html',context)

def offer_product_edit(request, id):
    if 'admin_id' in request.session:
        item = Product.objects.get(id=id)
        if request.method == 'POST':
            if request.POST['product_offer'] == '' or len(request.POST['product_offer']) > 2 or int(request.POST['product_offer'])>70:
                messages.error(request,'Productoffer is not valid!! and must be below 70%', extra_tags='productediterror')
                return render(request, 'admin/productofferedit.html', {'data':item})
            else:
                item.product_offer = request.POST['product_offer']
                item.save()
                return redirect(offer_product)
        return render(request, 'admin/productofferedit.html',{'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def offer_product_delete(request, id):
    item               = Product.objects.get(id=id)
    item.product_offer = 0
    item.save()
    return redirect(offer_product)

def user_delete(request, id):
    item=Accounts.objects.filter(id=id)
    item.delete()
    return redirect(listusers)


def categories(request):
    if 'admin_id' in request.session:
        item = Category.objects.all()
        return render(request, 'admin/categories.html', {'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def offer_category(request):
    if 'admin_id' in request.session:
        item = Category.objects.all().order_by("id")
        return render(request, 'admin/categoryoffer.html',{'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def offer_category_add(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        print(request.POST['category_name'])
        if request.POST['category_offer'] == '' or len(request.POST['category_offer']) > 2 or int(request.POST['category_offer'])>70:
            messages.error(request,'Category offer is not valid!! and must be below 70%', extra_tags='categoryadderror')
            return redirect(offer_category_add)
        elif request.POST['category_name'] == 'Select One':
            messages.error(request,'Please select a  category', extra_tags='categoryadderror')
            return redirect(offer_category_add)
        category            = request.POST['category_name']
        offer               = request.POST['category_offer']
        item                = Category.objects.get(category_name = category)
        item.category_offer = offer
        item.save()
        return redirect(offer_category)
    context = {
        'value':categories
    }
    return render(request, 'admin/categoryofferadd.html',context)

def offer_category_edit(request, id):
    if 'admin_id' in request.session:
        item = Category.objects.get(id=id)
        if request.method == 'POST':
            if request.POST['category_offer'] == '' or len(request.POST['category_offer']) > 2 or int(request.POST['category_offer'])>70:
                messages.error(request,'Categoryoffer is not valid!! and must be below 70%', extra_tags='categoryerror')
                return render(request, 'admin/categoryofferedit.html', {'data':item})
            else:
                item.category_offer = request.POST['category_offer']
                item.save()
                return redirect(offer_category)
        return render(request, 'admin/categoryofferedit.html',{'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def offer_category_delete(request, id):
    item               = Category.objects.get(id=id)
    item.category_offer = 0
    item.save()
    return redirect(offer_category)

def category_add(request):
    if 'admin_id' in request.session:
        if request.method == 'POST':
            category_name = str(request.POST['category_name'])
            category_name = category_name.upper()
            description = request.POST['description']
            if Category.objects.filter(category_name = category_name):
                messages.error(request,'Category already exists!!',extra_tags='categoryerror')
                return redirect(category_add)
            elif request.POST['category_name'] == '' or request.POST['description'] == '':
                messages.error(request,'Categoryname must not be empty!!', extra_tags='categoryerror')
                return redirect(category_add)
            else:
                item = Category.objects.create(
                    category_name=category_name,
                    description=description
                )
                return redirect(categories)
        return render(request, 'admin/categoryadd.html')
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def category_edit(request, id):
    if 'admin_id' in request.session:
        item=Category.objects.get(id=id)
        if request.method == 'POST':
            if Category.objects.filter(category_name = request.POST['category_name']) and request.POST['category_name']!= item.category_name:
                messages.error(request,'Category already exists!!',extra_tags='categoryerror')
                return render(request, 'admin/categoryedit.html', {'data':item})
            elif request.POST['category_name'] == '' or request.POST['description'] == '':
                messages.error(request,'Categoryname must not be empty!!', extra_tags='categoryerror')
                return render(request, 'admin/categoryedit.html', {'data':item})
            else:
                item.category_name = request.POST['category_name']
                item.description = request.POST['description']
                item.save()
                return redirect(categories)
        else:
            return render(request, 'admin/categoryedit.html', {'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def category_delete(request, id):
    item = Category.objects.filter(id=id)
    item.delete()
    return redirect(categories)

def admin_login(request):
    if 'admin_id' in request.session:
        return redirect(home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        if username == '' and password == '':
            messages.error(request, 'Please enter the values!!!')
            return redirect(admin_login)
        elif username != 'admin':
            messages.error(request, 'Only admin can access!!!')
            return redirect(admin_login)
        elif Accounts.objects.filter(username = username):
            admin = authenticate(username = username, password = password)
            if admin is not None:
                request.session['admin_id'] = username
                login(request,admin)
                return redirect(home)
            else:
                messages.error(request, 'Invalid Credentials!!!')
                return redirect(admin_login)
        else:
            messages.error(request, 'Admin Credentials is invalid!!!')
            return redirect(admin_login)
    return render(request, 'admin/login.html')

def admin_logout(request):
    if 'admin_id' in request.session:
        del request.session['admin_id']
        logout(request)
        return redirect(admin_login)
    return render(request,'user/login.html')


def listusers(request):
    if 'admin_id' in request.session:
        if 'search' in request.GET:
            sh = request.GET['search']
            multiple_sh = Q(Q(first_name__icontains=sh) | Q(email__contains=sh))
            item = Accounts.objects.filter(multiple_sh).order_by("-id")
            return render(request, 'users.html',{'data':item})
        else:
            item = Accounts.objects.all().order_by("-id")
            return render(request, 'admin/userlist.html',{'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)
    
            


def blockuser(request,id):
    item = Accounts.objects.get(id = id)
    if item.is_active:
        item.is_active = False
    else:
        item.is_active = True
    item.save()
    return redirect(listusers)


def coupens(request):
    if 'admin_id' in request.session:
        item = Coupen.objects.all().order_by('coupencode')
        context={
            'data':item
        }
        return render(request, 'admin/coupen.html', context)
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def coupenAdd(request):
    if 'admin_id' in request.session:
        if request.method =='POST':
            coupen_code  = request.POST['coupen-code']
            coupen_price = request.POST['coupen-price']
            expiry_date  = request.POST['expiry_date']
            expiry_date  = datetime.strptime(expiry_date, '%m/%d/%Y').strftime('%Y-%m-%d')
            if coupen_code == '' or coupen_price == '' or expiry_date == '':
                messages.error(request, 'Code and price is mustnot be empty!!')
                return redirect(coupenAdd)
            elif int(coupen_price)>30 :
                messages.error(request, 'Offer must be below 30%!!')
                return redirect(coupenAdd)
            else:
                item = Coupen.objects.create(coupencode = coupen_code, coupen_offer = coupen_price, expiry_date=expiry_date)
                return redirect(coupens)

        return render(request, 'admin/coupenadd.html')
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def coupenEdit(request, id):
    if 'admin_id' in request.session:
        item = Coupen.objects.get(id=id)
        if request.method =='POST':
            coupen_code  = request.POST['coupen-code']
            expiry_date  = request.POST['expiry_date']
            coupen_price = request.POST['coupen-price']
            if coupen_code == '' or coupen_price == '':
                messages.error(request, 'Code and price is mustnot be empty!!')
                return redirect('/editcoupen/'+str(id))
            elif int(coupen_price)>30 :
                messages.error(request, 'Offer must be below 30%!!')
                return redirect('/editcoupen/'+str(id))
            else:
                item.coupencode   = coupen_code
                item.coupen_offer = coupen_price
                if expiry_date:
                    item.expiry_date  = expiry_date
                
                item.save()
                return redirect(coupens)
        else:
            context = {
                'data' : item
            }
        return render(request, 'admin/coupenedit.html', context)
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def coupenDelete(request, id):
    item = Coupen.objects.get(id=id)
    item.delete()
    return redirect(coupens)


def orders(request):
    if 'admin_id' in request.session:
        order_qs = Order.objects.filter(orderd = True).order_by('-id')
        return render(request, 'admin/orders.html',{'data' : order_qs})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def edit_status_View(request,id):
    if request.session.get('admin_id'):
        edit_status = Order.objects.get(id = id)
        print(edit_status.status)
        if edit_status.status   == 'Confirmed':
            print(edit_status.status)
            edit_status.status  = "Shipped"
        elif edit_status.status   == 'Shipped':
            print(edit_status.status)
            edit_status.status  = "Out for delivery"
        elif edit_status.status == 'Out for delivery':
            edit_status.status  = "Delivered"
            edit_status.date_delivered = datetime.now().date()
            for i in edit_status.items.all():
                item       = Product.objects.get(id=i.product.id)
                item.stock -= i.quantity
                item.save()
        edit_status.save()         
        return redirect (orders)
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def cancel_status_view(request,id):
    cancel_status = Order.objects.get(id = id)        
    cancel_status.status = "Canceled"
    cancel_status.save()
    return redirect(orders)

def salesreport(request):
    if 'admin_id' in request.session:
        item = Order.objects.filter(orderd=True)
        context = {
            'items' : item
            }
        return render(request, 'admin/salesreport.html', context)
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

def export_as_excel(request, value, tovalue, state):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=SalesReport' +\
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('SalesReport')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['user_name','payment_method', 'date_ordered', 'total_price']
    for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    if value != None and tovalue != None and state == 'date':
        print('hello')
        rows = Order.objects.filter(orderd=True, date_ordered__lte = tovalue, date_ordered__gte = value).values_list('user__username','payment_method',  'date_ordered', 'total_price')
    elif value != None and tovalue == None and state == 'month':
        rows = Order.objects.filter(orderd=True, date_ordered__month = value[1], date_ordered__year = value[0]).values_list('user__username','payment_method',  'date_ordered', 'total_price')
    elif value != None and tovalue == None and state == 'year':
        rows = Order.objects.filter(orderd=True, date_ordered__year = value).values_list('user__username','payment_method',  'date_ordered', 'total_price')
    else:
        rows = Order.objects.filter(orderd=True).values_list('user__username','payment_method',  'date_ordered', 'total_price')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
    
    wb.save(response)
    return response

def sort_with_date(request):
    if 'admin_id' in request.session:
        if request.method == 'GET':
            date_ls = request.GET['daterangenew']
            date    = ''
            todate  = ''
            month = request.GET['month']
            month = month.split('-')
            year  = request.GET['year']
            if month ==  [''] and year=='Select':
                print('hey')
                date_ls = date_ls.split(' - ')
                date = date_ls[0]
                date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
                todate = date_ls[1]
                todate = datetime.strptime(todate, '%m/%d/%Y').strftime('%Y-%m-%d')
            
            context = {}
            if (date == '' or todate ==  '') and month ==  [''] and year=='Select':
                print('Select any option')
                messages.error(request, 'please enter an input!!')
                return redirect(salesreport)
            else:
                if date != '' and  todate != '':
                    items = Order.objects.filter(orderd = True, date_ordered__lte = todate, date_ordered__gte = date)
                    context={
                        'date':date,
                        'todate':todate,
                        'items':items
                    }
                elif month != ['']:
                    items = Order.objects.filter(orderd = True, date_ordered__month = month[1], date_ordered__year = month[0] )
                    context = {
                        'month':month,
                        'items':items
                    }
                elif year != 'Select':
                    items = Order.objects.filter(orderd = True, date_ordered__year = year)
                    context = {
                        'year':year,
                        'items':items
                    }
                else:
                    print('fail')
                    return redirect(salesreport)
                print(year)
                return render(request, 'admin/salesreport.html', context)
        else:
            return redirect(salesreport)
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)

