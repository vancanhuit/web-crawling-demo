import urllib.request
from bs4 import BeautifulSoup
import os
import csv
import re

''' Demo web crawling with BeautifulSoup 4 '''


def not_relative_uri(href):
    return re.compile('^https://').search(href) is not None


def write_to_csv_file(feeds, filename, mode='w', write_header=False):
    with open(filename, mode) as csv_file:
        writer = csv.writer(csv_file)

        if write_header:
            writer.writerow(['Title', 'Link'])

        for feed in feeds:
            if feed.has_attr('target'):
                continue

            title = feed.get('title')
            link = feed.get('href')

            if title is None or link is None:
                continue

            writer.writerow([title, link])

url = 'https://vnexpress.net/'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

data_file = os.path.join(os.getcwd(), 'data', 'vnexpress_feeds.csv')

new_feeds = soup.find(
    'section', class_='featured container clearfix').find_all(
        'a', class_='', href=not_relative_uri)

sidebar_home_1 = soup.find('section', class_='sidebar_home_1').find_all(
    'a', class_='', href=not_relative_uri)

sidebar_home_2 = soup.find('section', class_='sidebar_home_2').find_all(
    'a', class_='', href=not_relative_uri)

write_to_csv_file(new_feeds, data_file, write_header=True)
write_to_csv_file(sidebar_home_1, data_file, mode='a')
write_to_csv_file(sidebar_home_2, data_file, mode='a')
