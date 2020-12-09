from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = "admin"

urlpatterns = [
    path('login/', admin_login, name = 'admin_login'),
    path('index/', admin_index, name = 'admin_main'),
    path('faq/', faq_manage, name = 'faq_manage'),
    path('order/', order_manage, name = 'order_manage'),
    path('order/detail/<int:id>', order_detail, name='order_detail'),
    path('logout/', admin_logout, name='admin_logout'),
    path('product/register/', product_register, name='product_register'),
    path('product/', product, name='product'),
    path('product/delete/<int:id>', product_delete, name='product_delete'),
    path('product/edit/<int:id>', product_edit, name='product_edit'),
    path('member/', member_manage, name='member'),
    path('update/<int:id>', member_update, name='info_update'),
    path('faq/', faq_manage, name='m2m_faq'),
    path('answer/<int:id>', answer_window, name='m2m_answer'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)