from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, AboutUs, SignUpView, ContactView, FaqView, PrivacyPolicyView, TermsOfUseView, \
    FilterByCategory, MyOrdersView, OrderDetail, ProductDetail, SPlOfferDetail, SearchView, CheckoutView,CreateOrder,PaymentView

app_name = 'src'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about-us/', AboutUs.as_view(), name='about-us'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('contact-us/', ContactView.as_view(), name='contact-us'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-of-use/', TermsOfUseView.as_view(), name='terms-of-use'),
    path('filter-by-category/', FilterByCategory.as_view(), name='filter-by-category'),
    path('my-orders/', MyOrdersView.as_view(), name='my-orders'),
    path('order-detail/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
    path('product-detail/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('spl-offer/<int:pk>/', SPlOfferDetail.as_view(), name='spl-offer'),
    path('search/', SearchView.as_view(), name='search'),
    path('cart/', CheckoutView.as_view(), name='cart'),
    path('create-order/', CreateOrder.as_view(), name='create-order'),
    path('payment/', PaymentView.as_view(), name='payment'),
]
