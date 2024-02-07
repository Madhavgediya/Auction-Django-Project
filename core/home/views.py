from django.shortcuts import redirect, render , get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import  logout as auth_logout
from .forms import RegistrationForm
from django.views.generic import ListView
from .forms import *

from .models import *

def home(request):
    product_data = Product.objects.all()
    # product_data = product_data[:3]
    # product_data = Product.objects[:3]
    product_data = Product.objects.order_by('-id')[:3]
    data = {
            'product_data':product_data,
        }
    return render(request, "home/index.html", data) 

def contact(request):
    context = {'page': 'Contact'}
    return render(request, "home/contact.html", context) 

def category(request):
    context = {'page': 'category'}
    category_data = Categorie.objects.all()
    # product_data = product_data[:3]
    # product_data = Product.objects[:3]
    category_data = Categorie.objects.all()
    data = {
            'category_data':category_data,
        }
    return render(request, "home/category.html", data) 

def about(request):
    about = {'page': 'About'}
    return render(request, "home/about.html", about) 

# def auction(request):
#     auctions = Auction.objects.all()
#     template_name = 'home/auction.html'
#     context = {'auctions': auctions}
#     return render(request, template_name, context)
def auctions(request):
    auctions = Auction.objects.all()

    # Determine the active status for each auction
    auction_data = []
    for auction in auctions:
        auction_data.append({
            'auction': auction,
            'is_active': auction.is_active(),
        })

    template_name = 'home/auction.html'
    context = {'auction_data': auction_data}
    return render(request, template_name, context)
   
#    Products Data Prototype
    # auction = {'page': 'Auction'}
    # product_data = Product.objects.all()
    # data = {
    #         'product_data':product_data
    #     }
    # return render(request, "home/auction.html", data) 

def user(request):
    user = {'page': 'user'}
    return render(request, "home/user.html", user) 

def mj(request):
    mj = {'page': 'mj'}
    return render(request, "home/#loginForm", mj) 


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Password Do not match")
            return redirect('home')

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        messages.success(request, "Success")
        return redirect('home')

def my_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login")
            return redirect('home')
        else:
            messages.error(request, "Not Login")
            return redirect('home')

    return HttpResponse('404 page')
    
def my_logout(request):
    auth_logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('home')

def auction_list_view(request):
    auctions = Auction.objects.all()
    template_name = 'home/auction_list.html'
    context = {'auctions': auctions}
    return render(request, template_name, context)

# class AuctionListView(ListView):
#     model = Auction
#     template_name = 'home/auction_list.html'
#     context_object_name = 'auctions'

def bid(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # Redirect the user to the login page or display an authentication message
        # Customize this based on your project's requirements
        return redirect('/#loginModal')  # Adjust 'login' to the actual login URL in your project

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']

            # Check bid constraints (first bid > base price, subsequent bids > previous bid amount)
            if auction.bids.exists():
                previous_bid = auction.bids.latest('bid_time')
                if bid_amount <= previous_bid.bid_amount:
                    form.add_error('bid_amount', 'Bid must be greater than the previous bid.')
                    return render(request, 'home/bid.html', {'form': form, 'auction': auction})

            # Create the bid
            user = request.user
            Bid.objects.create(auction=auction, user=user, bid_amount=bid_amount)
            # return redirect('auction_detail', auction_id=auction.id)
            return redirect('auction_detail', auction_id=auction.id)

    else:
        form = BidForm()

    return render(request, 'home/bid.html', {'form': form, 'auction': auction})

def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    # Get bids for the auction
    bids = auction.bids.all()

    context = {'auction': auction, 'bids': bids}
    return render(request, 'home/auction_detail.html', context)

def category_products(request, category_id):
    category = get_object_or_404(Categorie, pk=category_id)
    products_in_category = category.product_set.all()
    auctions = Auction.objects.filter(product__in=products_in_category)
    return render(request, 'home/category_products.html', {'category': category, 'auctions': auctions})
