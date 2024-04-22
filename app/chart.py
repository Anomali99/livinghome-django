
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.db.models import Count
from .models import Date, Link
from django.conf import settings
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.use('Agg') 

def getDatesAll(platform:str):
    intervals = [
        {
            'title': 'harian',
            'dateformat':'%d-%m-%y',
            'dates': Date.objects.filter(platform=platform).annotate(date_class=TruncDate('date')).values('date_class').annotate(total=Count('id')),
        },
        {
            'title': 'bulanan',
            'dateformat':'%b-%y',
            'dates': Date.objects.filter(platform=platform).annotate(date_class=TruncMonth('date')).values('date_class').annotate(total=Count('id')),
        },
        {
            'title': 'tahunan',
            'dateformat':'%Y',
            'dates': Date.objects.filter(platform=platform).annotate(date_class=TruncYear('date')).values('date_class').annotate(total=Count('id')),
        },
    ]
    return intervals

def getDatesByDate(platform:str, date1:datetime, date2:datetime):
    intervals = [
        {
            'title': 'harian',
            'dateformat':'%d-%m-%y',
            'dates': Date.objects.filter(platform=platform,date__range=(date1, date2)).annotate(date_class=TruncDate('date')).values('date_class').annotate(total=Count('id')),
        },
        {
            'title': 'bulanan',
            'dateformat':'%b-%y',
            'dates': Date.objects.filter(platform=platform,date__range=(date1, date2)).annotate(date_class=TruncMonth('date')).values('date_class').annotate(total=Count('id')),
        },
        {
            'title': 'tahunan',
            'dateformat':'%Y',
            'dates': Date.objects.filter(platform=platform,date__range=(date1, date2)).annotate(date_class=TruncYear('date')).values('date_class').annotate(total=Count('id')),
        },
    ]
    return intervals

def getDatesProduct(platform:str, idProduct):
    link = Link.objects.filter(id_product=idProduct).first()
    intervals = [
        {
            'title': 'harian',
            'dateformat':'%d-%m-%y',
            'dates': Date.objects.filter(platform=platform,id_link=link.id).annotate(date_class=TruncDate('date')).values('date_class').annotate(total=Count('id')),
        },
        {
            'title': 'bulanan',
            'dateformat':'%b-%y',
            'dates': Date.objects.filter(platform=platform,id_link=link.id).annotate(date_class=TruncMonth('date')).values('date_class').annotate(total=Count('id')),
        },
        {
            'title': 'tahunan',
            'dateformat':'%Y',
            'dates': Date.objects.filter(platform=platform,id_link=link.id).annotate(date_class=TruncYear('date')).values('date_class').annotate(total=Count('id')),
        },
    ]
    return intervals

def getDatesProductByDate(platform:str, idProduct, date1:datetime, date2:datetime):
    link = Link.objects.filter(id_product=idProduct).first()
    intervals = [
        {
            'title': 'harian',
            'dateformat':'%d-%m-%y',
            'dates': Date.objects.filter(platform=platform,id_link=link.id,date__range=(date1, date2)).annotate(date_class=TruncDate('date')).values('date_class').annotate(total=Count('id')),
        },
        {
            'title': 'bulanan',
            'dateformat':'%b-%y',
            'dates': Date.objects.filter(platform=platform,id_link=link.id,date__range=(date1, date2)).annotate(date_class=TruncMonth('date')).values('date_class').annotate(total=Count('id')),
        },
        {
            'title': 'tahunan',
            'dateformat':'%Y',
            'dates': Date.objects.filter(platform=platform,id_link=link.id,date__range=(date1, date2)).annotate(date_class=TruncYear('date')).values('date_class').annotate(total=Count('id')),
        },
    ]
    return intervals

def generateChart(result,max_range:int,platform:str,idUser) -> str:
    indexX = [link['date_class'].strftime(result['dateformat']) for link in result['dates']]
    indexY = [link['total'] for link in result['dates']]
    plt.bar(indexX, indexY)
    plt.gca().set_ylim(0, max_range)
    plt.xlabel('date')
    plt.ylabel('count')
    plt.title(f'click pada {platform} interval {result["title"]}')  
    filepath = os.path.join(settings.EXPORT_DIRS, f'{platform}_{result["title"]}_{str(idUser)}.png')
    try:
        plt.savefig(filepath)
    except Exception as e:
        print(f"Error saving image: {e}")
    plt.clf()
    return filepath