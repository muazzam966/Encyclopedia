from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from markdown2 import Markdown
markdowner = Markdown()

class Search(forms.Form):
    item=forms.CharField(label="Search for Entries" )

class Create(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.TextInput(attrs={'size': '50'})) 

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea)       

def index(request):
    entries=util.list_entries()
    if request.method=="POST":
        form=Search(request.POST)
        if form.is_valid():
            item=form.cleaned_data["item"]
            for entry in entries:
                if item == entry:
                    pageconv = util.get_entry(item)
                    page = markdowner.convert(pageconv)
                    return render(request, "encyclopedia/entrypage.html", {
                        "page": page,
                        "pagename": item.capitalize(),
                        "box": Search()
                    })
                if item.lower() in entry.lower():
                    return render(request, "encyclopedia/search.html", {
                        "entry" : entry,
                        "box": Search() 
                    })
            if item not in entries:
                return render (request, "encyclopedia/error.html", {
                        "box": Search()
                    })        
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "box": Search()
          })

def entrypage(request, title):
    entries=util.list_entries()
    if request.method=="POST":
        form=Search(request.POST)
        if form.is_valid():
            item=form.cleaned_data["item"]
            for entry in entries:
                if item == entry:
                    pageconv = util.get_entry(item)
                    page = markdowner.convert(pageconv)
                    return render(request, "encyclopedia/entrypage.html", {
                        "page": page,
                        "pagename": item.capitalize(),
                        "box": Search()
                    })
                if item.lower() in entry.lower():
                    return render(request, "encyclopedia/search.html", {
                        "entry" : entry,
                        "box": Search() 
                    })
            if item not in entries:
                return render (request, "encyclopedia/error.html", {
                        "box": Search()
                    })
    pageconv = util.get_entry(title)
    page = markdowner.convert(pageconv)                      
    return render(request, "encyclopedia/entrypage.html", {
            "page": page, 
            "pagename": title.upper(),
            "box": Search()
        })

def newpage(request):
    if request.method == 'POST':
        form = Create(request.POST["title", "textarea"])
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error2.html", {
                    "box": Search(),
                    "message": "Page already exist"})
            else:
                util.save_entry(title,textarea)
                pageconv = util.get_entry(title)
                page = markdowner.convert(pageconv) 
                return render(request, "encyclopedia/entrypage.html", {
                    "box": Search(),
                    "page": page, 
                    "pagename": title
                    }) 
    entries=util.list_entries()
    if request.method=="POST":
        form=Search(request.POST)
        if form.is_valid():
            item=form.cleaned_data["item"]
            for entry in entries:
                if item == entry:
                    pageconv = util.get_entry(item)
                    page = markdowner.convert(pageconv) 
                    return render(request, "encyclopedia/entrypage.html", {
                        "page": page,
                        "pagename": item.capitalize(),
                        "box": Search()
                    })
                if item.lower() in entry.lower():
                    return render(request, "encyclopedia/search.html", {
                        "entry" : entry,
                        "box": Search() 
                    })
            if item not in entries:
                return render (request, "encyclopedia/error.html", {
                        "box": Search()
                    })                        
    
    return render(request, "encyclopedia/create.html", {
        "box": Search(),
        "create": Create()
        })    


def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "box": Search(), 
            "edit":Edit(initial={'textarea': page})
                
             })
       
    else:
        form = Edit(request.POST) 
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            pageconv = util.get_entry(title)
            page = markdowner.convert(pageconv) 
            return render(request, "encyclopedia/entrypage.html", {
                "box": Search(),
                "page": page, 
                "pagename": title
                })


 
def randompage(request):

    entries = util.list_entries()
    num = random.randint(0, len(entries) - 1)
    page_random = entries[num]
    pageconv = util.get_entry(page_random)
    page = markdowner.convert(pageconv) 

    return render(request, "encyclopedia/entrypage.html", {
        "page": page,
        "box": Search(),
        "pagename": page_random
    })
