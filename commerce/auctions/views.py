from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Watchlist


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

def create(request):
    #Getting a new listing
    if request.method == "POST":
        #Test inputs

        #Create new listing
        item = Listing(
            name = request.POST['name'],
            description = request.POST['description'],
            price = request.POST['price'],
            owner = request.user
        )
        item.save()

        return HttpResponseRedirect(reverse("index"))

    #Loading the page
    return render(request, "auctions/create.html")

def listing(request, list_id):

    listing = Listing.objects.get(id = list_id)

    #TODO Server Side Validation of new bids
    
    if request.method == "POST":
        listing.bids += 1
        listing.price = request.POST['bid']
        listing.buyer = request.user
        listing.save()

    return render(request, "auctions/listing.html", {
        "listing": listing
    })

def close(request, list_id):
    listing = Listing.objects.get(id = list_id)
    listing.active = False
    listing.save()

    return HttpResponseRedirect(reverse("index"))

def watch(request, user_name):
    newUser = User.objects.get(username = user_name)
    watching = Watchlist.objects.filter(
        watch_user = newUser, 
        item__active = True)

    print("NewUser ID: ", newUser.id)
    print("Watching: ", watching)

    return render(request, "auctions/watchlist.html", {
        "listings": watching
    })

def watch_add(request, user_name, list_id):
    user = User.objects.get(username = user_name)
    item = Listing.objects.get(id = list_id)
    watchlist = Watchlist(watch_user = user, item = item)
    watchlist.save()

    return HttpResponseRedirect(reverse("watch", kwargs = {
        "user_name": user.username
    }))