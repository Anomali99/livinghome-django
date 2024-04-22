from .chart import generateChart, getDatesAll, getDatesByDate, getDatesProduct, getDatesProductByDate
from urllib.parse import quote
from datetime import datetime, timedelta
from django.db.models import Count
from .models import Date
import random

def getWALink(no: str, title: str) -> str:
    noWA = int(no)
    text = ("Assalamualaikum.\n" +
            f"saya ingin membeli {title} apakah masih ada ?"
            )
    sub = quote(text)
    link = f'https://wa.me/62{str(noWA)}?text={sub}'
    return link

def generateLink(id) -> str:
    generate = ''.join(random.choices('0123456789', k=10))  
    return f'{generate}{str(id)}'

def getRangeAll() -> int:
    results = Date.objects.values('platform').annotate(total=Count('platform'))
    max_count = 10 
    for result in results:
        if max_count < result['total']:
            max_count = result['total']
    return max_count

def getRange(date1: datetime, date2: datetime) -> int:
    results = Date.objects.filter(date__range=(date1, date2)).values('platform').annotate(total=Count('platform'))
    max_count = 10
    for result in results:
        if max_count < result['total']:
            max_count = result['total']
    return max_count

def getChartAll(idUser):
    image_uris = []
    max_range = getRangeAll()
    for x in ['web', 'ig', 'fb']:
        for result in getDatesAll(x):
            filepath = generateChart(result,max_range,x,idUser)
            image_uris.append(filepath)
    return image_uris

def getChartProduct(idUser,idProduct):
    image_uris = []
    max_range = getRangeAll()
    for x in ['web', 'ig', 'fb']:
        for result in getDatesProduct(x,idProduct):
            filepath = generateChart(result,max_range,x,idUser)
            image_uris.append(filepath)
    return image_uris

def getChartByDate(idUser,date1:datetime,date2:datetime):
    image_uris = []
    max_range = getRange(date1=date1,date2=date2)
    for x in ['web', 'ig', 'fb']:
        for result in getDatesByDate(x,date1,date2):
            filepath = generateChart(result,max_range,x,idUser)
            image_uris.append(filepath)
    return image_uris

def getChartProductByDate(idUser,idProduct,date1:datetime,date2:datetime):
    image_uris = []
    max_range = getRange(date1=date1,date2=date2)
    for x in ['web', 'ig', 'fb']:
        for result in getDatesProductByDate(x,idProduct,date1,date2):
            filepath = generateChart(result,max_range,x,idUser)
            image_uris.append(filepath)
    return image_uris