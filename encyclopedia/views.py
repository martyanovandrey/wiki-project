from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def my_content(request, title):
    title_md = util.get_entry(title)
    title_html = markdown2.markdown(title_md)

    return render(request, "encyclopedia/title.html", {
        "title": title_html
    })

def search_wiki(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    if any(query.lower() == val.lower() for val in entries):
        title_md = util.get_entry(query)
        title_html = markdown2.markdown(title_md)
        return render(request, "encyclopedia/title.html", {
            "title": title_html
        })
    else:
        match_list = [s for s in entries if query.lower() in s.lower()]
        return render(request, "encyclopedia/match.html", {
        "entries": match_list
    })

class NewContent(forms.Form):
    title = forms.CharField(label='Create title')
    content = forms.CharField(label='Create content')

def create_new_page(request):
    return render(request, "encyclopedia/new_page.html")

def new_page(request):
    if request.method == 'POST':
        form = NewContent(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            entries = util.list_entries()
            if any(title.lower() == val.lower() for val in entries):
                return HttpResponseNotFound('<h1>Title already taken.</h1>') 
            else:
                content = form.cleaned_data['content']
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseNotFound('<h1>Fields can\'t be empty.</h1>')
    return HttpResponseNotFound('<h1>Request method should be \"POST\"</h1>')
