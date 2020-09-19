from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.utils.html import strip_tags

class NewContent(forms.Form):
    title = forms.CharField(label='Create title', widget=forms.TextInput(attrs={'class' : 'title_style'}))
    content = forms.CharField(widget=forms.Textarea(), label='Create content')

class EditContent(forms.Form):
    title = forms.CharField(label='Create title')
    content = forms.CharField(label='Create content')

#List of all pages
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Load page from .md file and convert to html.
def my_content(request, title):
    title_md = util.get_entry(title)
    title_html = markdown2.markdown(title_md)
    title_load = strip_tags(title_html)
    return render(request, "encyclopedia/title.html", {
        "title": title_html,
        'title_load': title_load
    })

#Get query from search bar, look for matches and return result or list or similar results.
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

#Create new page
def new_page(request):
    if request.method == 'POST':
        form = NewContent(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            #Create content and add Title in it
            content = (f'#{title}\n\n') + form.cleaned_data['content']
            entries = util.list_entries()
            #Search if title already taken
            if any(title.lower() == val.lower() for val in entries):
                return HttpResponseNotFound('<h1>Error: Title already taken.</h1>') 
            else:
                util.save_entry(title, content)
                return my_content(request, title)
        else:
            return HttpResponseNotFound('<h1>Error: Fields can\'t be empty.</h1>')
    else:
        return render(request, "encyclopedia/new_page.html", {
            'form': NewContent()
        })
 
def edit_page(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        context = {
            'title': title,
            'content': content
        }

        return render(request, "encyclopedia/edit_page.html", context)
    else:
        return render(request, "encyclopedia/edit_page.html", {
        "edit_page": util.get_entry(title)
    })  