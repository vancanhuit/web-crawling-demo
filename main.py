import urllib.request
from bs4 import BeautifulSoup
import os
import csv
import re
from datetime import datetime

''' Demo web crawling with BeautifulSoup 4 '''


def not_relative_uri(href):
    return re.compile('^https://').search(href) is not None


def add_feeds(feeds):
    for feed in feeds:
        # Do some filters before adding
        if feed.has_attr('target'):
            continue

        title = feed.get('title')
        link = feed.get('href')
        if title is None or link is None:
            continue

        total_feeds.add((title, link))


def write_to_csv_file(filename):
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title', 'Link'])

        for feed in total_feeds:
            writer.writerow(feed)

        print('All feeds were stored in file {}'.format(filename))

url = 'https://vnexpress.net/'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

total_feeds = set()

today = datetime.date(datetime.now()).isoformat()
data_file = os.path.join(
    os.getcwd(), 'data', 'vnexpress_feeds_' + today + '.csv')

new_feeds = soup.find(
    'section', class_='featured container clearfix').find_all(
        'a', class_='', href=not_relative_uri)

sidebar_home_1_feeds = soup.find('section', class_='sidebar_home_1').find_all(
    'a', class_='', href=not_relative_uri)

sidebar_home_2_feeds = soup.find('section', class_='sidebar_home_2').find_all(
    'a', class_='', href=not_relative_uri)

add_feeds(new_feeds)
add_feeds(sidebar_home_1_feeds)
add_feeds(sidebar_home_2_feeds)

write_to_csv_file(data_file)
