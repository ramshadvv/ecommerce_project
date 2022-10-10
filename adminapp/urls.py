from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='adminhome'),
    path('categories/', views.categories, name='categories'),
    path('categoryoffer/', views.offer_category, name='categoryoffer'),
    path('addcategoryoffer/', views.offer_category_add, name='addcategoryoffer'),
    path('editcategoryoffer/<int:id>/', views.offer_category_edit, name='editcategoryoffer'),
    path('deletecategoryoffer/<int:id>/', views.offer_category_delete, name='deletecategoryoffer'),
    path('addcategory/', views.category_add, name='addcategory'),
    path('editcategory/<int:id>/', views.category_edit, name='editcategory'),
    path('deletecategory/<int:id>/', views.category_delete, name='deletecategory'),
    path('product/', views.products, name='product'),
    path('productoffer/', views.offer_product, name='productoffer'),
    path('addproductoffer/', views.offer_product_add, name='addproductoffer'),
    path('editproductoffer/<int:id>/', views.offer_product_edit, name='editproductoffer'),
    path('deleteproductoffer/<int:id>/', views.offer_product_delete, name='deleteproductoffer'),
    path('addproduct/', views.product_add, name='addproduct'),
    path('editproduct/<int:id>/', views.product_edit, name='editproduct'),
    path('deleteproduct/<int:id>', views.product_delete, name='deleteproduct'),
    path('coupen/', views.coupens, name='coupen'),
    path('addcoupen/', views.coupenAdd, name='addcoupen'),
    path('editcoupen/<int:id>', views.coupenEdit, name='editcoupen'),
    path('deletecoupen/<int:id>', views.coupenDelete, name='deletecoupen'),
    path('login/', views.admin_login, name='adminlogin'),
    path('adminlogout/', views.admin_logout, name='adminlogout'),
    path('listsusers/', views.listusers, name='listusers'),
    path('deleteuser/<int:id>/', views.user_delete, name='deleteuser'),
    path('blockuser/<int:id>/', views.blockuser, name='blockuser'),
    path('orders/', views.orders, name='orders'),
    path('editstatus/<int:id>/', views.edit_status_View, name='editstatus'),
    path('cancelstatus/<int:id>/', views.cancel_status_view, name='cancelstatus'),
    path('salesreport/', views.salesreport, name='salesreport'),
    path('export_as_excel/', views.export_as_excel, name='export_as_excel'),
    path('sort_with_date/', views.sort_with_date, name='sort_with_date'),
]