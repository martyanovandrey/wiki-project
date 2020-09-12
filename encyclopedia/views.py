from django.shortcuts import render
from . import util
import markdown2


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
    if query:
        title_md = util.get_entry(query)
        title_html = markdown2.markdown(title_md)
        return render(request, "encyclopedia/title.html", {
            "title": title_html
        })
