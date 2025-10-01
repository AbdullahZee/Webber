from bs4 import BeautifulSoup
from package import web
import sys

x = input("Enter a URl: ")

target = web.site(x)

urls = target.scrap()
print(urls)