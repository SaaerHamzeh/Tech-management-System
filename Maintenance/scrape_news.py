import requests
from bs4 import BeautifulSoup
from .models import News

def scrape_bbc_arabic():
    url = 'https://www.bbc.com/arabic'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.find_all('h3')[:5]

    for h in headlines:
        title = h.text.strip()
        link_tag = h.find('a')
        if link_tag:
            link = 'https://www.bbc.com' + link_tag['href']
        else:
            continue

        # تأكد ما تكرر الخبر
        if not News.objects.filter(title=title).exists():
            News.objects.create(
                title=title,
                link=link,
                source='BBC Arabic'
            )
