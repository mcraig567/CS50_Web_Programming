from django.shortcuts import render
from markdown2 import Markdown
markdowner = Markdown()

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": markdowner.convert(util.get_entry(title)), 
#        "entry": "<h1>HTML</h1>",
        "title": title
   })