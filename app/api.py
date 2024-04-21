from .models import Link, Date, Product
from .generate import getWALink
from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime

def webLink(request, token):
    link = Link.objects.filter(web_link=token).first()
    if link:
        click = link.web_click
        link.web_click = click + 1
        link.save()
        date = Date.objects.create(
            platform = 'web',
            date = datetime.now(),
            id_link = link,
            )
        date.save()
        walink = getWALink(link.no_wa,link.id_product.title)
        return HttpResponseRedirect(walink)
    else:
        return render(request,'app/404.html')

def igLink(request, token):
    link = Link.objects.filter(ig_link=token).first()
    if link:
        click = link.ig_click
        link.ig_click = click + 1
        link.save()
        date = Date.objects.create(
            platform = 'ig',
            date = datetime.now(),
            id_link = link,
            )
        date.save()
        walink = getWALink(link.no_wa,link.id_product.title)
        return HttpResponseRedirect(walink)
    else:
        return render(request,'app/404.html')

def fbLink(request, token):
    link = Link.objects.filter(fb_link=token).first()
    if link:
        click = link.fb_click
        link.fb_click = click + 1
        link.save()
        date = Date.objects.create(
            platform = 'fb',
            date = datetime.now(),
            id_link = link,
            )
        date.save()
        walink = getWALink(link.no_wa,link.id_product.title)
        return HttpResponseRedirect(walink)
    else:
        return render(request,'app/404.html')