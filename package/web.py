from bs4 import BeautifulSoup
import sys
import requests
from requests import codes


class site():
    codes = [
            200, 201, 202, 203, 204, 205, 206, 207, 208, 226,
            300, 301, 302, 303, 304, 305, 307, 308
        ]
    def __init__(self, url):
        self.url = url

    def scrap(self):
        try:
            res = requests.get(self.url)
        except:
            raise Exception

        urls = set()
        scraped_urls = set()
        misc = set()

        key = self.url.split('.')[-2:]
        key = ".".join(key)

        if res.status_code in self.codes:
            soup = BeautifulSoup(res.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                urls.add(link['href'])
            scraped_urls.add(res.url)
        else:
            print('Negative response.')
            raise Exception

        print(urls)
        for urls2 in urls:
            if key in urls2 or res.url in urls2:
                scraped_urls.add(urls2)
                try:
                    res2 = requests.get(urls2)
                    if res2.status_code in self.codes:
                        soup2 = BeautifulSoup(res2.content, 'html.parser')
                        for link in soup2.find_all('a', href=True):
                            if key in link:
                                scraped_urls.add(link['href'])
                            else:
                                misc.add(link['href'])

                except:
                    pass
            else:
                misc.add(urls2)


        main, sub, mail, tel, others = set()

        for x in urls, scraped_urls, misc:
            for url in x:
                if key in url and res.url not in url:
                    sub.add(url)
                elif key in url and res.url in url:
                    main.add(url)
                elif 'mailto' in url:
                    url = url.split(':')[1]
                    mail.add(url)
                elif 'tel' in url:
                    url = url.split(':')[1]
                    tel.add(url)
                elif '/' in url[:1] and '/' in url[-1:]:
                    make = self.url + url
                    main.add(make)
                else:
                    others.add(url)

        print('MAIN'.center(10, '-'))
        for val in main:
            print(val)
        print('SUB DOMAINS'.center(10, '-'))
        for val in sub:
            print(val)
        print('MAILS'.center(10, '-'))
        for val in mail:
            print(val)
        print('TEL NUMBERS'.center(10, '-'))
        for val in tel:
            print(val)
        print('OTHERS'.center(10, '-'))
        for val in others:
            print(val)


