from django.contrib.auth import authenticate, login, logout
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

#Make logged in only?
def create(request):
    #Getting a new listing
    if request.method == "POST":
        #Test inputs
        #Need to ensure that URL is valid

        #Save new listing
        item = Listing(
            name = request.POST['name'],
            description = request.POST['description'],
            price = request.POST['price'],
            owner = request.user
        )

        #Add optional category if specified by user
        if request.POST['category'] != 'None':
            item.category = request.POST['category']

        #Add image if specified by user
        if request.POST['image'] != "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg":
            item.image = request.POST['image']

        item.save()

        return HttpResponseRedirect(reverse("index"))

    #Loading the page, 
    return render(request, "auctions/create.html", {
        "categories": category_list
    })

def listing(request, list_id):

    listing = Listing.objects.get(id = list_id)
    comments = Comment.objects.filter(item__id = list_id)

    #TODO Server Side Validation of new bids
    
    if request.method == "POST":
        listing.bids += 1
        listing.price = request.POST['bid']
        listing.buyer = request.user
        listing.save()     


    wishlists = Watchlist.objects.filter(
        watch_user = request.user,
        item = listing
    )

    print(wishlists)
    print("Length: ", len(wishlists))

    if len(wishlists) == 0:
        wish = False
    else:
        wish = True

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "wish": wish,
        "active": listing.active
    })

def close(request, list_id):
    listing = Listing.objects.get(id = list_id)
    listing.active = False
    listing.save()

    return HttpResponseRedirect(reverse("index"))

def watch(request, user_name):

    newUser = User.objects.get(username = user_name)
    watching = Watchlist.objects.filter(watch_user = newUser)

    print("NewUser ID: ", newUser.id)
    print("Watching: ", watching)

    return render(request, "auctions/watchlist.html", {
        "listings": watching
    })

def watch_add(request, user_name, list_id):
    user = User.objects.get(username = user_name)
    item = Listing.objects.get(id = list_id)

    watchCheck = Watchlist.objects.filter(
        watch_user = user,
        item = item
    )

    if len(watchCheck) == 0:
        watchlist = Watchlist(watch_user = user, item = item)
        watchlist.save()

    else:
        watchCheck.delete()

    return HttpResponseRedirect(reverse("watch", kwargs = {
        "user_name": user.username
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
    return render(request, "auctions/index.html", {
        "listings": listings
    })