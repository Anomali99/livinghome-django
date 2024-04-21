from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from .models import Product, Image, Link
from datetime import datetime
import os

# Create your views here.
def home(request):
    context = {
        'login': request.session.get('login'),
        'products': [],
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
        Link.objects.create(
            no_wa = wa,
            web_link = '0',
            fb_link = '0',
            ig_link = '0',
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
