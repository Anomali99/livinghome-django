from urllib.parse import quote
import random

def getWALink(no: str, title: str) -> str:
    noWA: int = int(no)
    text: str = ("Assalamualaikum.\n" +
            f"saya ingin membeli {title} apakah masih ada ?"
            )
    sub: str = quote(text)
    link: str = f'https://wa.me/62{str(noWA)}?text={sub}'
    return link

def generateLink(id:int) -> str:
    generate: str = ''.join(random.choices('0123456789', k=10))  
    return f'{generate}{str(id)}'


def getRange(result) -> int:
    max_range: int = 10
    for count in result['dates'] :
        if count['total'] > max_range:
            max_range = count['total'] + 10
    return max_range