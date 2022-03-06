from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

def clean(html):
    return " ".join(html.split())

def conv_char(c):
    conv = {
        'a':'áâãäåæ',
        'c':'ç',
        'e':'èéêë',
        'i':'ìîíï',
        'o':'óòõôö',
        'u':'ùúûü'
    }
    
    for key in conv:
        if c in conv[key]:
            return key
    return c    
        
def conv_name(name):
    name = name.lower()
    new_name = ''
    for c in name:  
        new_name += conv_char(c)
    return new_name

def get_soup(url):
    try:
        response = urlopen(url)
        html = response.read().decode('utf-8')
    except:
        return 'error'
    return BeautifulSoup(html, 'html.parser')

def get_name_info(soup):
    meaning_tags = soup.find('div', id='significado').findAll('p', limit=2)
    meaning = ''
    for i in range(len(meaning_tags)):
        meaning += meaning_tags[i].get_text() + '\n' if i > 0 else meaning_tags[i].get_text().split(':')[1] + '\n'
    source_tag = soup.find('p', id='origem')
    source = source_tag.get_text().split(':')[1] if source_tag else ''
    return meaning.strip(), source.strip() 

def get_page_names(soup, baseurl):
    cards  = soup('a', class_ = 'full-w')
    name_list = []
    for card in cards:
        name = card.span.get_text()
        url = baseurl + card.get('href')
        soup = get_soup(url)
        if soup == 'error':
            continue
        meaning, source = get_name_info(soup)
        name_list.append({'nome':name,'significado':meaning, 'origem': source, 'url': url})
    return name_list

def is_the_end(soup):
    return soup.find('a', class_ = 'pag-btn--next') == None

def get_all_names(filename, query_url):
    page = 1
    name_list = []
    baseurl = 'https://www.dicionariodenomesproprios.com.br'
    
    while True:
        soup = get_soup(url + f'{page}/')
        name_list += get_page_names(soup, baseurl)
        
        if is_the_end(soup):
            break
            
        print(f'Página {page} completa!')
        page += 1
    df = pd.DataFrame(sorted(name_list, key = lambda x: conv_name(x['nome'])))
    df.to_csv (filename, index = None, header=True)
    
if __name__ == '__main__':
    filename = input('Nome do Arquivo:')
    url = input('Url:')
    get_all_names(filename, url)