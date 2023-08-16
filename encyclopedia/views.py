from django.shortcuts import render
import markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def md_to_html(title):
    content = util.get_entry(title)
    md = markdown.Markdown()
    if content == None:
        return None
    else:
        return md.convert(content)

def entry(request, title):
    page_content = md_to_html(title)
    if page_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page doesn't exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": page_content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST["q"]
        page_content = md_to_html(entry_search)
        if page_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": page_content
            })
        else:
            entries = util.list_entries()
            reccomendations = []
            for entry in entries:
                if entry_search.lower() in entry.lower():
                    reccomendations.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendet": reccomendations
            })

def create_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create_page.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        titleExists = util.get_entry(title)
        if titleExists is not None:
            return render (request, "encyclopedia/error.html", {
                "message": "Page already exists"
            })
        else:
            util.save_entry(title, content)
            page_content = md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": page_content
            })

def edit_page(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })

def save_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        page_content = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": page_content
        })

def random_page(request):
    entries = util.list_entries()
    rand_page = random.choice(entries)
    page_content = md_to_html(rand_page)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_page,
        "content": page_content
    })
