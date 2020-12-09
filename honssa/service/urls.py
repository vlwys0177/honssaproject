from django.urls import path, include
from .views import *

app_name = 'service'

urlpatterns=[
    path('', service_center, name='service_main'),
    path('board/', service_board, name='service_board'),
    path('m2m/', m2m_list, name='m2m_list'),
    path('m2m/<int:id>', m2m_detail, name='m2m_detail'),
    path('faq/', service_faq, name='service_faq'),
]