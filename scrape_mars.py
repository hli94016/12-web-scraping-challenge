from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import pprint
import time

def scrape_info():
  executable_path = {'executable_path': ChromeDriverManager().install()}
  browser = Browser('chrome', **executable_path, headless=False)

  marsUrl = 'https://redplanetscience.com'
  newsTitle, newsParagraph = scrapeMarsNews(browser, marsUrl)

  featureUrl = 'https://spaceimages-mars.com'
  feature_image_url = scrapeFeatureImage(browser, featureUrl)

  marsFactsUrl = 'https://galaxyfacts-mars.com/'
  marsFactsTable = scrapMarsFacts(marsFactsUrl)

  marsHemispheresUrl = 'https://marshemispheres.com/'
  imageUrls = scrapMarsHermispheres(browser, marsHemispheresUrl)

  # print(imageUrls)
  data = {
    'news_title': newsTitle,
    'news_paragraph': newsParagraph
    'feature_image_url': feature_image_url,
    'marsFacts': marsFactsTable,
    'hemispheresImageUrls': imageUrls
  }
  # print(data)
  # pprint.pprint(data)
  browser.quit()
  return data

def scrapeMarsNews(browser, url):
  browser.visit(url)
  # HTML object
  html = browser.html
  # Parse HTML with Beautiful Soup
  soup = BeautifulSoup(html, 'html.parser')

  list_div = soup.find_all('div', class_='list_text')[0]
  contentTitle = list_div.find('div', class_='content_title')
  contentBody = list_div.find('div', class_='article_teaser_body')
  newsTitle = contentTitle.get_text()
  newsParagraph = contentBody.get_text()

  return newsTitle, newsParagraph

def scrapeFeatureImage(browser, url):
  browser.visit(url)
  # HTML object
  html = browser.html
  # Parse HTML with Beautiful Soup
  soup = BeautifulSoup(html, 'html.parser')
  header_div = soup.find('div', class_='header')

  header_image = header_div.find('img', class_='headerimage')
  feature_image_url = url + header_image['src']
  return feature_image_url

def scrapMarsFacts(url):
  df = pd.read_html(url)[0]
  df.columns=['Description', 'Mars', 'Earth']
  return df.to_html(classes=["table"])

def scrapMarsHermispheres(browser, url):
  browser.visit(url)
  # HTML object
  html = browser.html
  # Parse HTML with Beautiful Soup
  soup = BeautifulSoup(html, 'html.parser')
  result_list_div = soup.find('div', class_='result-list')

  imageUrls = []
  for item_div in result_list_div.find_all('div', class_='item'):
    href_elem = item_div.find_all(href=True)[0]
    hemisphereDict = {}
    title_elem = item_div.find('h3')
    title = title_elem.get_text()
    hemisphereDict['title'] = title
    link = url + href_elem['href']
    browser.visit(link)
    soup = BeautifulSoup(browser.html, 'html.parser')

    download_div = soup.find('div', class_='downloads')
    image_href_elem = download_div.find_all(href=True)[0]
    href = image_href_elem['href']

    hemisphereDict['image_url'] = url + image_href_elem['href']
    imageUrls.append(hemisphereDict)
    browser.back()

  return imageUrls