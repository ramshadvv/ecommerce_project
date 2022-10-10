from cartapp.models import *
from productapp.models import *


def add_variable_to_context(request):
    if 'user_id' in request.session:
        user = request.session['user_id']
        order_qs = Order.objects.filter(user__username=user,orderd = False)
        wishlist_count = MyWishList.objects.filter(username__username=user).count()
        category = Category.objects.all()
        total_amount=0
        cart_count =0
        if order_qs.exists():
            orders = order_qs[0]
            total_amount = float(orders.total_amount_cart)
            cart_count = orders.items.count()
        tax = (total_amount) * 3 /100
        return {
            'total_amount':total_amount,
            'tax': tax,
            'tax_amount':total_amount+tax,
            'cart_count': cart_count,
            'wishlist_count':wishlist_count,
            'category':category
        }
    elif request.session.session_key:
        user = request.session.session_key
        order_qs = Order.objects.filter(items__guest_user = user,orderd = False)
        wishlist_count = MyWishList.objects.filter(username__username=user).count()
        category = Category.objects.all()
        total_amount=0
        cart_count =0
        if order_qs.exists():
            orders = order_qs[0]
            total_amount = float(orders.total_amount_cart)
            cart_count = orders.items.count()
        tax = (total_amount) * 3 /100
        return {
            'total_amount':total_amount,
            'tax': tax,
            'tax_amount':total_amount+tax,
            'cart_count': cart_count,
            'wishlist_count':wishlist_count,
            'category':category
        }
    else:
        
        category = Category.objects.all()
        return {
            'total_amount':0,
            'tax_amount':0,
            'tax': 0,
            'cart_count': 0,
            'wishlist_count':0,
            'category':category
        }
        

def checkid(request):
    if 'user_id' in request.session:
        logi = request.session.get('user_id')
        if Accounts.object.filter(username = logi):
            id = Accounts.object.get(username = logi)
        else:
            id = None
        return {
            'id' : id
        }
    else:
        return {'id':None}


def userdetails(request):
    if 'user_id' in request.session:
        logi = request.session.get('user_id')
        if Accounts.object.filter(username = logi):
            item = Accounts.object.get(username = logi)
            if CustomerAdress.objects.filter(user_id=item.id):
                add = CustomerAdress.objects.filter(user_id=item.id)
                ad_count = add.count()
                if add:
                    return {
                        'users' : item,
                        'address':add,
                        'ad_count':ad_count
                    }
                else:
                    return {
                        'users' : None,
                        'address':None,
                        'ad_count':None
                    }
            elif Accounts.object.filter(username = logi):
                return {
                    'users': item,
                    'address':None,
                    'ad_count':None
                }
            else:
                return {
                    'users':None,
                    'address':None,
                    'ad_count':None
                }
        else:
            return {
                'users':None,
                'address':None,
                'ad_count':None
            }
    else:
        return {
            'users' : None,
            'address':None,
            'ad_count':None
        }
    
    