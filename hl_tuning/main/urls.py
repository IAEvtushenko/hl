from django.urls import path

from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('<str:brand>', MainView.as_view(), name='works_for_exact_brand'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('lk/', LKView.as_view(), name='lk'),
    path('shop/', ShopMainView.as_view(), name='shop_main'),
    path('shop/product/<str:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('shop/add-to-cart/<str:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('shop/remove-from-cart/<str:pk>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('shop/change-qty/<str:pk>/', ChangeQTYView.as_view(), name='change_qty'),
    path('cart/', CartView.as_view(), name='cart'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('products/<str:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('shop/category/<str:pk>/', CategoryView.as_view(), name='category'),
    path('shop/category/<str:category_pk>/<str:subcategory_pk>/', SubcategoryView.as_view(), name='subcategory'),
    path('project/<str:pk>/', ProjectDetailView.as_view(), name='project_detail'),
]