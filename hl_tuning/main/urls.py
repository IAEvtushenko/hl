from django.urls import path

from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('<str:brand>', MainView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('lk/', LKView.as_view(), name='lk'),
    path('shop/', ShopMainView.as_view(), name='shop_main'),
    path('shop/product/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('shop/add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('shop/remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('shop/change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('cart/', CartView.as_view(), name='cart'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('products/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('shop/category/<str:slug>/', CategoryView.as_view(), name='category'),
    path('shop/category/<str:category_slug>/<str:subcategory_slug>/', SubcategoryView.as_view(), name='subcategory'),
    path('project/<str:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]