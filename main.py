import urllib.request
from bs4 import BeautifulSoup
import os
import csv

''' Demo web crawling with BeautifulSoup 4 '''
url = 'https://vnexpress.net/'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

feeds = []

# Get first feed of the day
new_feeds = soup.find('section', class_="featured container clearfix")
first_feed = new_feeds.find('a')
feeds.append((first_feed.get('title'), first_feed.get('href')))

# Get sub feeds beside first feed of the day
sub_feeds = new_feeds.find('div', class_='sub_featured').find(
    'ul', attrs={'id': 'list_sub_featured'}).find_all('a', class_="")
for feed in sub_feeds:
    feeds.append((feed.get('title'), feed.get('href')))


# Store into csv file
data_file = os.path.join(os.getcwd(), 'data', 'vnexpress_feeds.csv')
with open(data_file, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Title', 'Link'])

    for f in feeds:
        writer.writerow(f)
