from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.urls import reverse
from django.utils.html import strip_tags
from django.shortcuts import redirect
import random

class NewContent(forms.Form):
    title = forms.CharField(label='Create title', widget=forms.TextInput(attrs={'class' : 'title_style'}))
    content = forms.CharField(widget=forms.Textarea(), label='Create content')

#List of all pages
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Load page from .md file and convert to html.
def my_content(request, title):
    title_md = util.get_entry(title)
    if title_md == None:
        return render(request, "encyclopedia/index.html", {
            'error': 'We do not have an article on this topic yet, let\'s see what we got:',
            "entries": util.list_entries()
        })
    title_html = markdown2.markdown(title_md)
    title_load = strip_tags(title_html)
    return render(request, "encyclopedia/title.html", {
        'title': title_html,
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
    print(request.POST)
    if request.method == 'POST':
        #Create forms (title, content) from NewContent class
        form = NewContent(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            #Create content and add Title in it
            content = (f'#{title}\n\n') + form.cleaned_data['content']
            entries = util.list_entries()
            page_type = request.POST.get('page_type')
            #Search if title already taken if new page created and pass if edit page
            if any(title.lower() == val.lower() for val in entries) and page_type == 'new_page':
                return HttpResponseNotFound('<h1>Error: Title already taken.</h1>') 
            else:
                util.save_entry(title, content)
                return my_content(request, title)
        else:
            return HttpResponseNotFound('<h1>Error: Not valid data entered.</h1>')
    else:
        return render(request, "encyclopedia/new_page.html", {
            'form': NewContent()
        })

#Edit pages 
def edit_page(request, title):
    if request.method == 'GET':
        #Get content text and delete first 2 line (title and empty line)
        page = util.get_entry(title).split("\n",2)[2]
        context = {
            'title': title,
            'content': page
        }
        return render(request, "encyclopedia/edit_page.html", {
            'form': NewContent(initial=context)
        })
    else:
        return render(request, "encyclopedia/edit_page.html", {
        "edit_page": util.get_entry(title)
    })  

#Random page
def random_page(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect('/wiki/'+title)