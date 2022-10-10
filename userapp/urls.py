from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('categoryfilter/<str:value>/',views.selectedView,name='categoryfilter'),
    path('sortwithprice/<str:value>/<str:category>/',views.sortwithprice,name='sortwithprice'),
    path('product/<int:id>/', views.product_details, name='userproduct'),
    path('otpverification/',views.otp_verification,name='otpverification'),
    path('logout/',views.user_logout,name='logout'),
    path('login/',views.user_login,name='login'),
    path('otpverificationpassword/',views.otpverificationpassword,name='otpverificationpassword'),
    path('passwordverification/',views.passwordverification,name='passwordverification'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),
    path('otplogin/',views.otp_login,name='otplogin'),
    path('otpverificationphone/',views.otp_verification_phone,name='otpverificationphone'),
    path('signup/',views.signup,name='signup'),
    path('addaddress/',views.addaddress,name='addaddress'),
    path('editaddress/<int:id>/',views.edit_address,name='editaddress'),
    path('deleteaddress/<int:id>/',views.delete_address,name='deleteaddress'),
    path('wishlist/',views.wishlistview,name='wishlist'),
    path('wishlistadd/<int:id>/',views.wishlistadd,name='wishlistadd'),
    path('wishlistdelete/<int:id>/',views.wishlistdelete,name='wishlistdelete'),
    path('deletewishlistitem/<int:id>/',views.wishlistitemdelete,name='deletewishlistitem'),
    path('cart/',views.cartview,name='cart'),
    path('addcart/',views.cartadd,name='addcart'),
    path('deletecartitem/<int:item_id>/',views.deleteFromCart,name='deletecartitem'),
    path('addcartquantity/',views.changeQuantity,name='addcartquantity'),
    path('checkout/',views.checkoutview,name='checkout'),
    path('razorpay_checkout/',views.razorpay_checkout,name = "razorpay_checkout"),
    path('placing/',views.order_placingView,name='placing'),
    path('placed/',views.placed,name='placed'),
    path('profile/',views.profile,name='profile'),
    path('editprofile/',views.profileedit,name='editprofile'),
    path('orders/',views.myorders,name='userorders'),
    path('deleteorderitem/<int:item_id>/<int:order_id>/',views.cancelFromOrder,name='deleteorderitem'),
    path('cancelstatus/<int:id>/', views.cancel_status_view, name='usercancelstatus'),
    path('returnstatus/<int:id>/', views.return_status_view, name='userreturnstatus'),
    path('invoice/<int:id>/', views.invoice, name='invoice'),
    path('test/',views.test,name='test'),
]