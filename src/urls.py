from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView,AboutUs,SignUpView

app_name = 'src'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about-us/', AboutUs.as_view(), name='about-us'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),

]
