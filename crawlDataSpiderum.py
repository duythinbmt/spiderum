import bs4
import pandas
import requests

urls = []
for page in range(1, 32):
    urls.append("https://spiderum.com/s/khoa-hoc-cong-nghe/hot?page=" +
                str(page) + "#")

author = []
title = []
body = []
date = []
votes = []
views = []
links = []

for url in urls:

    def get_page_content(url):
        page = requests.get(url, headers={"Accept-Language": "en-US"})
        soup = bs4.BeautifulSoup(page.text, "html.parser")
        return soup

    soup = get_page_content(url)

    for inner in soup.findAll("div", class_="inner"):
        if inner.find('a', class_='username') == None:
            break
        author.append(inner.find('a', class_='username').string.strip())
        title.append(inner.find('h3', class_='title').find('a').string)
        body.append(inner.find('a', class_='body').string)
        date.append(inner.find('div', class_="created").find('span').string)
        votes.append(
            inner.find('div', class_="toolbar clearfix").find(
                'span', class_="vote-count").string)
        views.append(
            inner.find('div',
                       class_="toolbar clearfix").find('span',
                                                       class_="text").string)
        links.append("https://spiderum.com" +
                     inner.find('a', class_='body').get('href'))

df = pandas.DataFrame({
    "Title": title,
    "Author": author,
    "Vote": votes,
    "Views": views,
    "Link": links,
    "Body": body,
    "Date release": date
})
df.to_csv("spiderukm_khcn.csv", encoding='utf-8')
