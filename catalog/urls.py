from django.urls import path

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.conf.urls import url
from catalog.views import base_view, category_view, product_view, \
    cart_view, add_to_cart_view, remove_from_cart_view, change_item_qty, order_view, make_order_view, private_str_view,\
    registration_view, login_view, delete_product_view, add_product_view, index_view,\
    detail_order_view, form_doc_view

urlpatterns = [
    url(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
    url(r'^add_to_cart/$', add_to_cart_view, name='add_to_cart'),
    url(r'^change_item_qty/$', change_item_qty, name='change_item_qty'),
    url(r'^cart/$', cart_view, name='cart'),
    url(r'^order/$', order_view, name='create_order'),
    url(r'^private_page/$', private_str_view, name='private_page'),
    url(r'^make_order/$', make_order_view, name='make_order'),
    url(r'^registration/$', registration_view, name='registration'),
    url(r'^login/$', login_view, name='login'),
    url(r'^add/$', add_product_view, name='add'),
    url(r'^order/(?P<order_slug>[-\w]+)/$', detail_order_view, name='order_detail'),
    path('order/<slug:slug>/doc/<int:id>/', form_doc_view),
    # url(r'^order/(?P<order_slug>[-\w]+)/$', detail_order_view, name='detail'),
    path('catalog/delete/<int:id>/', delete_product_view),
    url(r'^thanks/$', TemplateView.as_view(template_name="thanks.html"), name='thanks'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
    url(r'^remove_from_cart/$', remove_from_cart_view, name='remove_from_cart'),
    url(r'^catalog/$', base_view, name='base'),
    url(r'^$', index_view, name='index')
]
