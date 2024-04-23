from .models import Product, Date, Link
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
import random

def dummy(request, token):
    products = Product.objects.all()
    total_click = int(token)
    result = []

    click_count = 0
    while click_count < total_click:
        product = products[random.randint(1, len(products)-1)]
        link = Link.objects.filter(id_product=product.id).first()
        if link:
            tgl = f'{str(random.randint(1, 28)).zfill(2)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(2023, 2024))} 00:00:00' 
            my_datetime = timezone.make_aware(timezone.datetime.strptime(tgl, "%d-%m-%Y %H:%M:%S"), timezone.get_current_timezone())
            platform = random.choice(['web','ig','fb'])
            if platform == 'web':
                webClick = link.web_click
                link.web_click = webClick + 1
            elif platform == 'fb':
                fbClick = link.fb_click
                link.fb_click = fbClick + 1
            elif platform == 'ig':
                igClick = link.ig_click
                link.ig_click = igClick + 1
            link.save()
            date = Date.objects.create(platform=platform,date=my_datetime,id_link=link)
            date.save()
            result.append({
                "platform": platform,
                "date": tgl,
                "id_link": link.id,
            })
        click_count = click_count + 1
    return JsonResponse(result, safe=False)

def remove(request):
    dates = Date.objects.all()
    dates.delete()
    for link in Link.objects.all():
        link.web_click = 0
        link.fb_click = 0
        link.ig_click = 0
        link.web_checkout = 0
        link.fb_checkout = 0
        link.ig_checkout = 0
        link.save()
    return JsonResponse({'message':"berhasil hapus"}, safe=False)