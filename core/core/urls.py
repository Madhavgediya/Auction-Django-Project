"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from core import settings
from home.views import auction_detail
from home.views import *


urlpatterns = [
    path('', home, name="home" ),
    path('category/', category, name="category" ),
    path('contact/', contact, name="contact" ),
    path('about/', about, name="about" ),
    path('auctions/', auctions, name="auctions" ),
    path('user/', user, name="user" ),
    path('mj/', mj, name="mj" ),
    path('admin/', admin.site.urls),
    path('register', register, name='register'),
    path('login', my_login_view, name='login'),
    path('logout', my_logout, name='logout'),
    path('auction_list_view/', auction_list_view, name='auction_list_view'),
    path('bid/<int:auction_id>/', bid, name='bid'),
    path('auction/<int:auction_id>/', auction_detail, name='auction_detail'),
    path('category/<int:category_id>/', category_products, name='category_products'),
    path('winner/<int:auction_id>/', winner, name='winner'),  
    path('my_bids/', my_bids, name='my_bids'),
    path('my_winnings/', my_winnings, name='my_winnings'),
    path('submit_your_product/', submit_your_product, name='submit_your_product'),
    path('my_products/', my_products, name='my_products'),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
