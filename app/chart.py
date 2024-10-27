
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.db.models import Count
from .models import Date, Link
from .generate import getRange
from django.conf import settings
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.use('Agg') 

def getDatesAll(chartInterval:str,style:str,idUser:int) -> list[str]:
    intervals: list[Date] = []
    for x in ['web', 'ig', 'fb']:
        if chartInterval == '1':
            intervals.append({
                'title': 'tahunan',
                'dateformat':'%Y',
                'platform':x,
                'dates': Date.objects.filter(platform=x).annotate(date_class=TruncYear('date')).values('date_class').annotate(total=Count('id')),
            })
        elif chartInterval == '2':
            intervals.append({
                'title': 'bulanan',
                'dateformat':'%b-%y',
                'platform':x,
                'dates': Date.objects.filter(platform=x).annotate(date_class=TruncMonth('date')).values('date_class').annotate(total=Count('id')),
            })
        elif chartInterval == '3':
            intervals.append({
                'title': 'harian',
                'dateformat':'%d-%m-%y',
                'platform':x,
                'dates': Date.objects.filter(platform=x).annotate(date_class=TruncDate('date')).values('date_class').annotate(total=Count('id')),
            })
    return generateChart(style,intervals,idUser)

def getDatesByDate(chartInterval:str,style:str,idUser:int,date1:datetime,date2:datetime) -> list[str]:
    intervals: list[Date] = []
    for x in ['web', 'ig', 'fb']:
        if chartInterval == '1':
            intervals.append({
                'title': 'tahunan',
                'dateformat':'%Y',
                'platform':x,
                'dates': Date.objects.filter(platform=x,date__range=(date1, date2)).annotate(date_class=TruncYear('date')).values('date_class').annotate(total=Count('id')),
            })
        elif chartInterval == '2':
            intervals.append({
                'title': 'bulanan',
                'dateformat':'%b-%y',
                'platform':x,
                'dates': Date.objects.filter(platform=x,date__range=(date1, date2)).annotate(date_class=TruncMonth('date')).values('date_class').annotate(total=Count('id')),
            })
        elif chartInterval == '3':
            intervals.append({
                'title': 'harian',
                'dateformat':'%d-%m-%y',
                'platform':x,
                'dates': Date.objects.filter(platform=x,date__range=(date1, date2)).annotate(date_class=TruncDate('date')).values('date_class').annotate(total=Count('id')),
            })
    return generateChart(style,intervals,idUser)

def getDatesProduct(chartInterval:str,style:str,idUser:int,idProduct:int) -> list[str]:
    link = Link.objects.filter(id_product=idProduct).first()
    intervals: list[Date] = []
    for x in ['web', 'ig', 'fb']:
        if chartInterval == '1':
            intervals.append({
                'title': 'tahunan',
                'dateformat':'%Y',
                'platform':x,
                'dates': Date.objects.filter(platform=x,id_link=link.id).annotate(date_class=TruncYear('date')).values('date_class').annotate(total=Count('id')),
            })
        elif chartInterval == '2':
            intervals.append({
                'title': 'bulanan',
                'dateformat':'%b-%y',
                'platform':x,
                'dates': Date.objects.filter(platform=x,id_link=link.id).annotate(date_class=TruncMonth('date')).values('date_class').annotate(total=Count('id')),
            })
        elif chartInterval == '3':
            intervals.append({
                'title': 'harian',
                'dateformat':'%d-%m-%y',
                'platform':x,
                'dates': Date.objects.filter(platform=x,id_link=link.id).annotate(date_class=TruncDate('date')).values('date_class').annotate(total=Count('id')),
            })
    return generateChart(style,intervals,idUser)

def getDatesProductByDate(chartInterval:str,style:str,idUser:int,idProduct:int,date1:datetime,date2:datetime) -> list[str]:
    link = Link.objects.filter(id_product=idProduct).first()
    intervals: list[Date] = []
    for x in ['web', 'ig', 'fb']:
        if chartInterval == '1':
            intervals.append({
                'title': 'tahunan',
                'dateformat':'%Y',
                'platform':x,
                'dates': Date.objects.filter(platform=x,id_link=link.id,date__range=(date1, date2)).annotate(date_class=TruncYear('date')).values('date_class').annotate(total=Count('id')),
            })
        elif chartInterval == '2':
            intervals.append({
                'title': 'bulanan',
                'dateformat':'%b-%y',
                'platform':x,
                'dates': Date.objects.filter(platform=x,id_link=link.id,date__range=(date1, date2)).annotate(date_class=TruncMonth('date')).values('date_class').annotate(total=Count('id')),
            })
        elif chartInterval == '3':
            intervals.append({
                'title': 'harian',
                'dateformat':'%d-%m-%y',
                'platform':x,
                'dates': Date.objects.filter(platform=x,id_link=link.id,date__range=(date1, date2)).annotate(date_class=TruncDate('date')).values('date_class').annotate(total=Count('id')),
            })
    return generateChart(style,intervals,idUser)

def generateChart(style:str,results:list[Date],idUser:int) -> list[str]:
    filepaths: list[str] = []
    for result in results:
        indexX: list[str] = [link['date_class'].strftime(result['dateformat']) for link in result['dates']]
        indexY: list[int] = [link['total'] for link in result['dates']]
        # plt.figure(figsize = (19, 10))
        if style == '1':
            plt.plot(indexX, indexY)
        elif style == '2':
            plt.bar(indexX, indexY)
        plt.gca().set_ylim(0, getRange(result))
        plt.xlabel('date')
        plt.ylabel('count')
        plt.title(f'click pada {result["platform"]} interval {result["title"]}')  
        filepath: str = os.path.join(settings.EXPORT_DIRS, f'{result["platform"]}Chart_{str(idUser)}.png')
        try:
            plt.savefig(filepath)
        except Exception as e:
            print(f"Error saving image: {e}")
        plt.clf()
        filepaths.append(filepath)
    return filepaths