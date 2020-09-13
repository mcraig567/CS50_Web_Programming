from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Watchlist

category_list = ['home', 'garden', 'sports']

def index(request):
    listings = Listing.objects.filter(active = True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    #Test inputs
    create_pass = True
    if request.method == "POST":
        if len(request.POST['name']) > 64:
            message = "Item name has a maximum 64 characters"
            create_pass = False
        elif float(request.POST['price']) < 0:
            message = "Your asking price must be at least $0.00"
            create_pass = False
        elif float(request.POST['price']) >= 9999999.99:
            message = "The maximum bid is $9999999.99, please lower your asking price"
            create_pass = False
        elif len(request.POST['description']) > 200:
            message = "Item description has a maximum 200 characters"
            create_pass = False

        #Save new listing
        item = Listing(
            name = request.POST['name'],
            description = request.POST['description'],
            price = request.POST['price'],
            owner = request.user
        )

        #Add optional category if specified by user
        if request.POST['category'] != 'None':
            if request.POST['category'] in category_list:
                item.category = request.POST['category']
            else:
                item.category = 'None'

        #Add image if specified by user
        if request.POST['image'] != "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg":
            item.image = request.POST['image']

        if create_pass == True:
            item.save()
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "auctions/create.html", {
                "categories": category_list,
                "message": message
            })

    #Loading the page
    return render(request, "auctions/create.html", {
        "categories": category_list
        })



def listing(request, list_id):

    listing = Listing.objects.get(id = list_id)
    comments = Comment.objects.filter(item__id = list_id)

    if request.user.is_authenticated:
        wishlists = Watchlist.objects.filter(
            watch_user = request.user,
            item = listing
        )
    else:
        wishlists = []

    if len(wishlists) == 0:
        wish = False
    else:
        wish = True    
    
    if request.method == "POST":

        #Validation of bid size
        if float(request.POST['bid']) > 9999999.99:
            message = "I don't think you have that much money! Max bid is $9999999.99"
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "wish": wish,
                "message": message
            })

        elif float(request.POST['bid']) <= listing.price:
            message = "You must bid higher than the current bid"
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "wish": wish,
                "message": message
            })

        #Bid is okay, add to database
        else:
            listing.bids += 1
            listing.price = request.POST['bid']
            listing.buyer = request.user
            listing.save()    

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "wish": wish,
    })

def close(request, list_id):
    listing = Listing.objects.get(id = list_id)
    listing.active = False
    listing.save()

    return HttpResponseRedirect(reverse("index"))

@login_required
def watch(request, user_name):

    #Don't let users view other people's watchlists
    if user_name != request.user.username:
        return HttpResponseRedirect(reverse("watch", kwargs={
            "user_name": request.user.username
        }))

    newUser = request.user
    watching = Watchlist.objects.filter(watch_user = newUser)

    return render(request, "auctions/watchlist.html", {
        "listings": watching
    })

@login_required
def watch_add(request, user_name, list_id):
    #Cannot add to another users watchlist, set user to logged in user
    user = request.user
   
    #Ensure that listing exists
    if len(Listing.objects.filter(id = list_id)) == 1:
        item = Listing.objects.get(id = list_id)

    else:
        message = "This listing does not exist"

        return HttpResponseRedirect(reverse("index"))


    watchCheck = Watchlist.objects.filter(
        watch_user = user,
        item = item
    )

    #Turn watchlist on and off
    if len(watchCheck) == 0:
        watchlist = Watchlist(watch_user = user, item = item)
        watchlist.save()

    else:
        watchCheck.delete()

    return HttpResponseRedirect(reverse("listing", kwargs = {
        "list_id": item.id
    }))

def comment(request, list_id):
    if request.method == "POST":
        listing = Listing.objects.get(id = list_id)
        user = request.user
        left_comment = request.POST["comment"]

        newComment = Comment(comment = left_comment, leaver = user, item = listing)
        newComment.save()

    return HttpResponseRedirect(reverse("listing", kwargs = {
        "list_id": list_id
    }))

def categories(request):

    if request.method == "POST":
        #Ensure that cateogry is a real category, reload page with error otherwise
        if request.POST['category'] not in category_list:
            listings = Listing.objects.filter(active = True)
            message = "You must select an existing category"

            return render(request, "auctions/categories.html", {
                "categories": category_list,
                "listings": listings,
                "message": message
            })

        else:
            if request.POST['category'] == "None":
                listings = Listing.objects.filter(active = True)
            else:
                listings = Listing.objects.filter(category = request.POST['category'])

            return render(request, "auctions/categories.html", {
                "categories": category_list,
                "listings": listings
            })

    listings = Listing.objects.filter(active = True)

    return render(request, "auctions/categories.html", {
        "categories": category_list,
        "listings": listings
    })

def closed(request):
    listings = Listing.objects.filter(active = False)
    return render(request, "auctions/closed.html", {
        "listings": listings
    })