from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from .models import Product, Image, Link, Comment
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
            web_link = generateLink(id),
            fb_link = generateLink(id),
            ig_link = generateLink(id),
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
            return HttpResponseRedirect('/')
        elif user:
            message = 'password salah'
        else:
            message = 'username tidak ditemukan'
    context = {'message':message}
    return render(request,'app/admin.html',context)

def logout(request):
    request.session.pop('login')
    return HttpResponseRedirect('/')
