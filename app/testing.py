from .models import Product, Date, Link
from django.http import JsonResponse
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
            tgl = f'{str(random.randint(1, 28)).zfill(2)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(2020, 2023))}' 
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
            date = Date.objects.create(platform=platform,date=datetime.strptime(tgl, "%d-%m-%Y"),id_link=link)
            date.save()
            result.append({
                'platform': platform,
                'date': tgl,
                'id_link': link.id,
            })
    return JsonResponse(result)