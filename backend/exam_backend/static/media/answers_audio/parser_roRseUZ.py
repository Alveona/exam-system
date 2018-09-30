import urllib.request
from bs4 import BeautifulSoup

def get_html(url):
     response = urllib.request.urlopen(url)
     return response.read()

def parse(html):
     soup = BeautifulSoup(html, "html.parser")
     class = soup.find('h2')
     rows = table.find_all('tr')
     print(class)

def main():
    parse(get_html('http://habrahabr.ru/'))

if __name__ == '__main__':
    main()

