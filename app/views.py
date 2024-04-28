from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
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
        title: str = request.POST.get('title')
        price: str = request.POST.get('price')
        description: str = request.POST.get('description')
        wa: str = request.POST.get('wa')
        images = request.FILES.getlist('cover')
        product: Product = Product.objects.create(
            title = title,
            description = description,
            price = price,
        )
        product.save()
        id: Product = Product.objects.order_by('-id').first()
        Link.objects.create(
            no_wa = wa,
            web_link = generateLink(id.id),
            fb_link = generateLink(id.id),
            ig_link = generateLink(id.id),
            id_product = product,
        )
        index = 1
        for image in images:
            now: datetime = datetime.now().strftime("%y%m%d%H%M%S")
            filename: str = f"{now}{index}.{image.name.rsplit('.',1)[1]}"
            Image.objects.create(image_uri=filename, id_product=product)
            filepath: str = os.path.join(settings.UPLOAD_DIRS, filename)
            with open(filepath, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            index = index + 1
        return HttpResponseRedirect(f'/detail/{id.id}')
    return render(request, 'app/product.html')

def detail(request, id):
    product: Product = Product.objects.filter(id=int(id)).first()
    if product:
        if request.method == 'POST':
            type: str = request.POST.get('form_type')
            if type == 'addComment':
                name: str = request.POST.get('name')
                comment: str = request.POST.get('comment')
                new = Comment.objects.create(
                    name = name,
                    comment = comment,
                    id_product = product,
                    )
                new.save()
            elif type == 'update':
                action: str = request.POST.get('action')
                if action == 'update':
                    title: str = request.POST.get('title')
                    price: str = request.POST.get('price')
                    description: str = request.POST.get('description')
                    wa: str = request.POST.get('wa')
                    webCheckout: int = request.POST.get('webCheckout')
                    igCheckout: int = request.POST.get('igCheckout')
                    fbCheckout: int = request.POST.get('fbCheckout')
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
    message: str = ''
    if request.method == 'POST':
        username: str = request.POST.get('username')
        password: str = request.POST.get('password')
        user: User = User.objects.filter(username=username).first()
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
        idUser: int = request.session.get('idUser')
        titleProduct: str = None
        charts: list[str] = []
        menu: str = '1'
        menuChart: str = '1'
        chartInterval: str = '1'
        idProduct: str = '1'
        date1: datetime = datetime.now()
        date2: datetime = datetime.now()
        if request.method == 'POST':
            menu = request.POST.get('cbx-chart')
            menuChart = request.POST.get('chart-style')
            chartInterval = request.POST.get('chart-interval')
            if menu in ['3','4']:
                date1 = timezone.make_aware(timezone.datetime.strptime(f"{request.POST.get('date1')} 00:00:00", "%Y-%m-%d %H:%M:%S"), timezone.get_current_timezone())
                date2 = timezone.make_aware(timezone.datetime.strptime(f"{request.POST.get('date2')} 00:00:00", "%Y-%m-%d %H:%M:%S"), timezone.get_current_timezone())
                if menu == '3':
                    charts = getDatesByDate(chartInterval=chartInterval,style=menuChart,idUser=idUser,date1=date1,date2=date2)
                elif menu == '4':
                    idProduct: int = request.POST.get('id_product')
                    titleProduct: int = request.POST.get('title_product')
                    charts = getDatesProductByDate(chartInterval=chartInterval,style=menuChart,idUser=idUser,idProduct=idProduct,date1=date1,date2=date2)
            elif menu == '2':
                idProduct: int = request.POST.get('id_product')
                titleProduct: int = request.POST.get('title_product')
                charts = getDatesProduct(chartInterval=chartInterval,style=menuChart,idUser=idUser,idProduct=idProduct)
            else:
                charts = getDatesAll(chartInterval=chartInterval,style=menuChart, idUser=idUser)
        else:
            charts = getDatesAll(chartInterval=chartInterval,style=menuChart, idUser=idUser)
        
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
            'titleProduct':titleProduct,
        }
        return render(request,'app/monitoring.html',context)
