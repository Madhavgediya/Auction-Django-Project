from django.shortcuts import redirect, render , get_object_or_404
from django.http import HttpResponse , HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate, login
from django.contrib.auth import  logout as auth_logout
from django.views.generic import ListView
from .forms import *
from .models import *
from django.http import JsonResponse


def home(request):
    user_profile = None
    if request.user.is_authenticated and not isinstance(request.user, AnonymousUser):
        user_profile = UserProfile.objects.filter(user=request.user).first()
    # Fetch all products
    product_data = Product.objects.all()

    # Fetch all auctions
    all_auctions = Auction.objects.all()

    # Filter the last three active auctions
    active_auctions = [auction for auction in reversed(all_auctions) if auction.is_active()][:3]

    # Filter the recent completed auctions
    completed_auctions = [auction for auction in reversed(all_auctions) if not auction.is_active()][:3]

    # Fetch winner data for completed auctions and filter in reverse order
    winners_data = Winner.objects.filter(auction__in=completed_auctions).select_related('user', 'auction__product')
    winners_data = winners_data.order_by('-id')[:3]

    data = {
        'user_profile': user_profile,  # Added this line to include user_profile in the context
        'product_data': product_data,
        'active_auctions': active_auctions,
        'completed_auctions': completed_auctions,
        'winners_data': winners_data,
    }

    return render(request, "home/index.html", data)

def category(request):
    context = {'page': 'category'}
    category_data = Categorie.objects.all()
    data = {
            'category_data':category_data,
        }
    return render(request, "home/category.html", data) 

def about(request):
    about = {'page': 'About'}
    return render(request, "home/about.html", about) 

def auctions(request):
    auctions = Auction.objects.all()
    auction_data = []
    for auction in auctions:
        auction_data.append({
            'auction': auction,
            'is_active': auction.is_active(),
        })

    template_name = 'home/auction.html'
    context = {'auction_data': auction_data}
    return render(request, template_name, context)

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
    
def contact(request):
    if request.method == 'POST':
        form = ContectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ContectForm()

    return render(request, 'home/contact.html', {'form': form})



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

def bid(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    if not request.user.is_authenticated:
         return redirect('/#loginModal')  

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']

            if auction.bids.exists():
                previous_bid = auction.bids.latest('bid_time')
                if bid_amount <= previous_bid.bid_amount:
                    min_bid_amount = previous_bid.bid_amount + 1
                    form.add_error('bid_amount', f'Bid must be higher than {min_bid_amount}.')
                    return render(request, 'home/bid.html', {'form': form, 'auction': auction})
            else:
                 if bid_amount <= auction.product.products_base_price:
                    form.add_error('bid_amount', f'Bid must be higher than the base price ({auction.product.products_base_price}).')
                    return render(request, 'home/bid.html', {'form': form, 'auction': auction})

            user = request.user
            Bid.objects.create(auction=auction, user=user, bid_amount=bid_amount)

            if auction.has_ended():
                determine_winner(auction)
                return redirect('winner', auction_id=auction.id)
            

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


def winner(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    # Check if a winner already exists for this auction
    winner_exists = Winner.objects.filter(auction=auction).exists()

    # If no winner exists, call determine_winner function to ensure winner is determined
    if not winner_exists:
        determine_winner(auction)

    # Get the last winner for the auction
    winner = Winner.objects.filter(auction=auction).last()

    context = {'auction': auction, 'winner': winner}
    return render(request, 'home/winner.html', context)

def determine_winner(auction):
    # Get the last bid for the auction
    last_bid = Bid.objects.filter(auction=auction).order_by('-bid_time').first()

    if last_bid:
        # Create Winner entry
        Winner.objects.create(
            user=last_bid.user,
            bid_amount=last_bid.bid_amount,
            auction=auction
        )
        

def my_bids(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to view your bids.')
        return redirect('/#loginModal')

    user_bids = Bid.objects.filter(user=request.user).reverse()
    return render(request, 'home/my_bids.html', {'user_bids': user_bids})

def my_winnings(request):
    if not request.user.is_authenticated:
        return redirect('/#loginModal')

    user_winnings = Winner.objects.filter(user=request.user)
    return render(request, 'home/my_winnings.html', {'user_winnings': user_winnings})


def submit_your_product(request):
    if not request.user.is_authenticated:
        return redirect('/#loginModal')

    categories = Categorie.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()

            messages.success(request, 'Your product is submitted and in review. It will be published for auction once approved by admin.')
            return redirect('submit_your_product')

    else:
        form = ProductForm()

    return render(request, 'home/submit_your_product.html', {'form': form, 'categories': categories})

def my_products(request):
    if not request.user.is_authenticated:
        return redirect('/#loginModal')

    user_products = Product.objects.filter(created_by=request.user)

    for product in user_products:
        try:
            auction = Auction.objects.filter(product=product).latest('start_time')
            product.auction = auction

            if auction.has_ended():
                winner = Winner.objects.filter(auction=auction).first()
                product.winner = winner
        except Auction.DoesNotExist:
            product.auction = None
            product.winner = None

    return render(request, 'home/my_products.html', {'user_products': user_products})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product has an associated auction
    if Auction.objects.filter(product=product).exists():
        messages.warning(request, 'Cannot delete a product with an associated auction.')
        return HttpResponseForbidden("You cannot delete a product with an associated auction.")
    else:
        product.delete()
        messages.success(request, 'Product deleted successfully.')

    return redirect('my_products')

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('/#loginModal')

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'home/edit_profile.html', {'form': form})

def complete_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Save the form and associate it with the current user
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            # Redirect to the home page
            return redirect('home')
    else:
        form = UserProfileForm()

    return render(request, 'home/complete_profile.html', {'form': form})


# task Given by ripal sir
def info(request):
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/info')
    else:
        form = InfoForm()

    return render(request, 'home/info.html', {'form': form})

