from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from .models import Product, Image, Link, Comment
from .chart import getDatesAll, getDatesByDate, getDatesProduct, getDatesProductByDate
from datetime import datetime
from .generate import generateLink
import os

# Create your views here.
def home(request):
    context = {
        'login': request.session.get('login'),
        'products': Product.objects.all(),
    }
    return render(request, 'app/home.html', context)

def product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        description = request.POST.get('description')
        wa = request.POST.get('wa')
        images = request.FILES.getlist('cover')
        product = Product.objects.create(
            title = title,
            description = description,
            price = price,
        )
        product.save()
        id = Product.objects.order_by('-id').first()
        Link.objects.create(
            no_wa = wa,
            web_link = generateLink(id.id),
            fb_link = generateLink(id.id),
            ig_link = generateLink(id.id),
            id_product = product,
        )
        index = 1
        for image in images:
            now = datetime.now().strftime("%y%m%d%H%M%S")
            filename = f"{now}{index}.{image.name.rsplit('.',1)[1]}"
            Image.objects.create(image_uri=filename, id_product=product)
            filepath = os.path.join(settings.UPLOAD_DIRS, filename)
            with open(filepath, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            index = index + 1
    return render(request, 'app/product.html')

def detail(request, id):
    product = Product.objects.filter(id=int(id)).first()
    if product:
        if request.method == 'POST':
            type = request.POST.get('form_type')
            if type == 'addComment':
                name = request.POST.get('name')
                comment = request.POST.get('comment')
                new = Comment.objects.create(
                    name = name,
                    comment = comment,
                    id_product = product,
                    )
                new.save()
            elif type == 'update':
                action = request.POST.get('action')
                if action == 'update':
                    title = request.POST.get('title')
                    price = request.POST.get('price')
                    description = request.POST.get('description')
                    wa = request.POST.get('wa')
                    webCheckout = request.POST.get('webCheckout')
                    igCheckout = request.POST.get('igCheckout')
                    fbCheckout = request.POST.get('fbCheckout')
                    product.title = title
                    product.price = price
                    product.description =description
                    product.save()
                    link = Link.objects.filter(id_product=int(id)).first()
                    link.no_wa = wa
                    link.web_checkout = webCheckout
                    link.ig_checkout = igCheckout
                    link.fb_checkout = fbCheckout
                    link.save()
                elif action == 'delete':
                    product.delete()
                    return HttpResponseRedirect('/')
        context = {
            'login': request.session.get('login'),
            'product': product,
            'IPserver': request.get_host(),
        }
        return render(request,'app/detail.html',context)
    else:
        return render(request,'app/404.html')


def admin(request):
    if request.session.get('login'):
        return HttpResponseRedirect('/')
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            request.session['login'] = True
            request.session['idUser'] = user.id
            return HttpResponseRedirect('/')
        elif user:
            message = 'password salah'
        else:
            message = 'username tidak ditemukan'
    context = {'message':message}
    return render(request,'app/admin.html',context)

def logout(request):
    request.session.pop('login')
    request.session.pop('idUser')
    return HttpResponseRedirect('/')

def monitoring(request):
    if request.session.get('login') != True:
        return HttpResponseRedirect('/')
    else:
        idUser = request.session.get('idUser')
        charts = []
        menu = '1'
        menuChart = '1'
        chartInterval = '1'
        idProduct = '1'
        date1 = datetime.now()
        date2 = datetime.now()
        if request.method == 'POST':
            menu = request.POST.get('cbx-chart')
            menuChart = request.POST.get('chart-style')
            chartInterval = request.POST.get('chart-interval')
            if menu == '3':
                date1 = datetime.strptime(request.POST.get('date1'), "%Y-%m-%d") 
                date2 = datetime.strptime(request.POST.get('date2'), "%Y-%m-%d") 
                charts = getDatesByDate(chartInterval=chartInterval,style=menuChart,idUser=idUser,date1=date1,date2=date2)
            elif menu in ['2','4',]:
                idProduct = request.POST.get('id_product')
                if menu == '2':
                    charts = getDatesProduct(chartInterval=chartInterval,style=menuChart,idUser=idUser,idProduct=idProduct)
                elif menu == '4':
                    date1 = datetime.strptime(request.POST.get('date1'), "%Y-%m-%d") 
                    date2 = datetime.strptime(request.POST.get('date2'), "%Y-%m-%d") 
                    charts = getDatesProductByDate(chartInterval=chartInterval,style=menuChart,idUser=idUser,idProduct=idProduct,date1=date1,date2=date2)
            else:
                charts = getDatesAll(chartInterval=chartInterval,style=menuChart, idUser=idUser)
        else:
            charts = getDatesAll(chartInterval='1',style='1', idUser=idUser)

        context = {
            'login': request.session.get('login'),
            'products': Product.objects.all(),
            'charts': charts,
            'menu': menu,
            'idProduct':idProduct,
            'date_1':date1.strftime("%Y-%m-%d"),
            'date_2':date2.strftime("%Y-%m-%d"),
            'menuChart':menuChart,
            'chartInterval':chartInterval,
        }
        return render(request,'app/monitoring.html',context)
