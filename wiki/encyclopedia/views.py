from django.shortcuts import render
from markdown2 import Markdown
markdowner = Markdown()

from django.http import HttpResponseRedirect
from django.urls import reverse

import os
from random import random

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title not in util.list_entries():
        url = reverse("error", kwargs={'message': 1})
        return HttpResponseRedirect(url)

    return render(request, "encyclopedia/entry.html", {
        "entry": markdowner.convert(util.get_entry(title)), 
        "title": title,
   })

def search(request):
    if request.method == "POST":
        if request.POST['q'] in util.list_entries():
            url = reverse("entry", kwargs={'title': request.POST['q']})
            return HttpResponseRedirect(url)
            
        else:
            entries = util.list_entries()
            search_entries = []

            for entry in entries:
                if request.POST['q'].lower() in entry.lower():
                    search_entries.append(entry)

            return render(request, "encyclopedia/search.html", {
                "entries": search_entries
            })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")

    elif request.method == "POST":

#        Add section for if entry already exists
        if request.POST['new_name'] in util.list_entries():
            url = reverse("error", kwargs={'message': 2})
            return HttpResponseRedirect(url)


        title = request.POST['new_name'] + '.md'
        code = request.POST['new_entry']

        path_folder = r"C:\Users\craig\Documents\CS50\Web_Programming\search_pers\CS50_Web_Programming\wiki\entries"

        md_file = os.path.join(path_folder, title)

        with open(md_file, 'w') as f:
            f.write(code)
        f.close()

        return HttpResponseRedirect(reverse("index"))

def edit(request, title):
    if title not in util.list_entries():
        url = reverse("error", kwargs={'message': 1})
        return HttpResponseRedirect(url)  

    if request.method == "GET":
        
        path_folder = r"C:\Users\craig\Documents\CS50\Web_Programming\search_pers\CS50_Web_Programming\wiki\entries"
        md_file = os.path.join(path_folder, title) + '.md'

        with open(md_file, 'r') as f:
            old = f.read()
        f.close()

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "old": old
        })

    elif request.method == "POST":

        code = request.POST['edit_entry']
        print(code)

        path_folder = r"C:\Users\craig\Documents\CS50\Web_Programming\search_pers\CS50_Web_Programming\wiki\entries"
        md_file = os.path.join(path_folder, title) + '.md'

        with open(md_file, 'w') as f:
            f.write(code)
        f.close()
        
        return HttpResponseRedirect(reverse("index"))

def randsite(request):
    number = random()
    spot = int(len(util.list_entries()) * number)
    title = util.list_entries()[spot]

    url = reverse("entry", kwargs={'title': title})
    return HttpResponseRedirect(url)

def error(request, message):
    if message == 1:
        response = "Sorry, this page doesn't exist. Use the 'Create New Page' option to add to the wiki!"

    elif message == 2:
        response = "Unable to add new page as this entry already exists!"

    return render(request, "encyclopedia/error.html", {
        "response": response
    })
