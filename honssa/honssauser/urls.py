from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'honssauser'

urlpatterns=[
    path('main/', honssa_main, name='main'),
    path('main/<category>/', honssa_category, name='category'),
    path('cart/', honssa_cart,name='cart'),
    path('cart/insert', cart_insert, name='cart_insert'),
    path('cart/delete/<int:id>', cart_delete, name='cart_delete'),
    path('cart/pay/', honssa_payment,name='payment'),
    path('cart/pay/order/', honssa_order,name='pay_order'),
    path('cart/pay/create/', honssa_create, name='order_create'),
    path('product/<int:id>/', product_detail,name='product_detail'),
    path('service/', include('service.urls')),
    path('my/', include('mypage.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)