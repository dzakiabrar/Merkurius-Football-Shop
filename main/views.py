from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product

from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

# @login_required(login_url='/login')
# def show_main(request):
#     # news_list = Product.objects.all()
#     news_list = Product.objects.filter(user=request.user)  # hanya ambil data milik user login

#     context = {
#         'npm' : '2306275241',
#         'name': 'dzaki abrar',
#         'class': 'PBP C',
#         'news_list': news_list
#     }

#     return render(request, "main.html", context)

@login_required(login_url='/login')
def show_main(request):
    news_list = Product.objects.filter(user=request.user)

    context = {
        'npm' : '2306275241',
        'name': 'dzaki abrar',
        'class': 'PBP C',
        'news_list': news_list,
        'last_login': request.COOKIES.get('last_login'),  # ambil cookie
    }

    return render(request, "main.html", context)


def create_news(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        # simpan user login
        product = form.save(commit=False)
        product.user = request.user   # simpan user yang login

        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_news.html", context)

@login_required(login_url='/login')
def show_news(request, id):
    news = get_object_or_404(Product, pk=id)
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, "news_detail.html", context)

def show_xml(request):
     news_list = Product.objects.all()
     xml_data = serializers.serialize("xml", news_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    news_list = Product.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, news_id):
   try:
       news_item = Product.objects.filter(pk=news_id)
       xml_data = serializers.serialize("xml", news_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, news_id):
   try:
       news_item = Product.objects.get(pk=news_id)
       json_data = serializers.serialize("json", [news_item])
       return HttpResponse(json_data, content_type="application/json")
   except Product.DoesNotExist:
       return HttpResponse(status=404)
   
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

# def login_user(request):
#    if request.method == 'POST':
#       form = AuthenticationForm(data=request.POST)

#       if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('main:show_main')

#    else:
#       form = AuthenticationForm(request)
#    context = {'form': form}
#    return render(request, 'login.html', context)

#menerapkan cookie last login
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # bikin response redirect
            response = HttpResponseRedirect('/')

            # set cookie last_login
            response.set_cookie('last_login', str(timezone.now()))

            return response
    else:
        form = AuthenticationForm(request)

    context = {'form': form}
    return render(request, 'login.html', context)

# def logout_user(request):
#     logout(request)
#     return redirect('main:login')

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


# def addEmploye(request):

#     newlist =  Employe.objects.all()

#     return request
