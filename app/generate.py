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


def getRange(result) -> int:
    max_range = 10
    for count in result['dates'] :
        if count['total'] > max_range:
            max_range = count['total'] + 10
    return max_range

def getChartAll(style:str,idUser):
    image_uris = []
    for x in ['web', 'ig', 'fb']:
        results = getDatesAll(x)
        for result in results:
            filepath = generateChart(style,result,getRange(result),x,idUser)
            image_uris.append(filepath)
    return image_uris

def getChartProduct(style:str,idUser,idProduct):
    image_uris = []
    for x in ['web', 'ig', 'fb']:
        results = getDatesProduct(x,idProduct)
        for result in results:
            filepath = generateChart(style,result,getRange(result),x,idUser)
            image_uris.append(filepath)
    return image_uris

def getChartByDate(style:str,idUser,date1:datetime,date2:datetime):
    image_uris = []
    for x in ['web', 'ig', 'fb']:
        results = getDatesByDate(x,date1,date2)
        for result in results:
            filepath = generateChart(style,result,getRange(result),x,idUser)
            image_uris.append(filepath)
    return image_uris

def getChartProductByDate(style:str,idUser,idProduct,date1:datetime,date2:datetime):
    image_uris = []
    for x in ['web', 'ig', 'fb']:
        results = getDatesProductByDate(x,idProduct,date1,date2)
        for result in results:
            filepath = generateChart(style,result,getRange(result),x,idUser)
            image_uris.append(filepath)
    return image_uris