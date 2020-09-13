"""wiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from encyclopedia import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("encyclopedia.urls")),
    path('wiki/<str:title>', views.my_content, name='my_content' ),
    path('search_wiki/', views.search_wiki, name='search_wiki' ),
    path('new_page/', views.create_new_page, name='create_new_page'),
    path('new_page/add', views.new_page, name='new_page')
]
