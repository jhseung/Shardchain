import urllib2, json
from bs4 import BeautifulSoup
import time, random

data = {}

def scrape(link):
    req = urllib2.Request(link, headers={'User-Agent':"Chrome"})
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.findChildren('table')
    rows = tables[0].findChildren('tr')
    rows = rows[1:]
    print "Scraping link: " + link
    for row in rows:
        cells = row.findChildren('td')
        for i,cell in enumerate(cells):
            if i == 1:
                acct_id = cell.string
            if i==4:
                num_tx = cell.string
        print "account {0} has {1} transactions".format(acct_id, num_tx)
        data[acct_id] = num_tx

def scrape_links():
    link = "https://etherscan.io/accounts/"
    add_on = "?ps=100"

    page_num = 1
    while page_num < 101:
        check_link = "{0}{1}{2}".format(link,page_num,add_on)
        scrape(check_link)
        sleep_time = random.uniform(0,1)
        print "Sleeping for: {0} seconds".format(sleep_time)
        time.sleep(random.uniform(0,1))
        print "Finished page {0}".format(page_num)
        page_num += 1

scrape_links()

with open('data.json', 'w') as fp:
    json.dump(data, fp)
