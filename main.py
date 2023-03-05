# import bibliotek
import requests
from bs4 import BeautifulSoup
import webbrowser

# ustawienie adresu strony
url = input("Enter OLX page url: ")
prefix = 'https://www.olx.pl'
# pobranie strony za pomocą requests
page = requests.get(url)

# utworzenie obiektu BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')


class Offer:
    def __init__(self, link, full_price):
        self.link = link
        self.full_price = full_price

    def __str__(self):
        return self.link + " " + str(self.full_price)


# lista linków do ofert
links = []

page_number = 1

# pętla przechodząca przez wszystkie strony z ofertami
while True:

    # pobranie wszystkich ofert na danej stronie
    offers = soup.find_all('div', attrs={'data-cy': 'l-card'})

    # dla każdej oferty pobierz link i cenę
    for offer in offers:

        # link do oferty
        link = offer.find('a', class_='css-rc5s2u')['href']
        if link.startswith('https://'):
            continue
        # cena oferty
        offer_page = requests.get(prefix + link)
        offer_soup = BeautifulSoup(offer_page.content, 'html.parser')
        price = offer_soup.find('h3', class_='css-ddweki er34gjf0').text
        price = int(price.replace(' zł', '').replace(' ', ''))

        # czynsz oferty
        rent = 0
        rent_paragraphs = offer_soup.find_all('p', class_='css-b5m1rv er34gjf0')
        for rent_paragraph in rent_paragraphs:
            if rent_paragraph.text.startswith('Czynsz (dodatkowo): '):
                rent = rent_paragraph.text
        rent = float(rent.replace('Czynsz (dodatkowo): ', '').replace(' zł', '').replace(' ', '').replace(',', '.'))

        # całkowita cena oferty
        total_price = price + rent

        # jeżeli całkowita cena oferty nie przekracza 3200 zł to dodaj link do listy linków
        if total_price <= 3200:
            offer = Offer(prefix + link, total_price)
            links.append(offer)
    # sprawdź czy jest następna strona
    page_name = 'Page ' + str(page_number + 1)
    page_number += 1
    next_page = soup.find('li', attrs={'aria-label': page_name})
    if next_page is None:
        break
    print("Going to next page " + page_name)
    # jeżeli jest następna strona to pobierz ją i przejdź do następnej iteracji pętli
    next_page_url = prefix + next_page.find('a')['href']
    page = requests.get(next_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

# sort list of offers by price
links.sort(key=lambda x: x.full_price)

while True:
    print("There are " + str(len(links)) + " offers")
    print("Choose range of offers to open in browser")
    print("From: ")
    from_index = int(input())
    print("To: ")
    to_index = int(input())
    for i in range(from_index, to_index):
        webbrowser.open_new_tab(links[i].link)