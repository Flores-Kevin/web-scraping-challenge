import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import numpy as np

def scrape_data():
    # Declare data sources
    url1 = "https://redplanetscience.com"
    url2 = "https://galaxyfacts-mars.com/"
    url3 = "https://marshemispheres.com/"
    url4 = "https://spaceimages-mars.com/"
    # Make a table full of facts from earth and mars
    tables = pd.read_html(url2)
    df1 = tables[0]
    df1 = df1.rename(columns={0:" ",1:'Mars',2:"Earth"})
    # Make a path for browser to visit and scrape data from latest news article
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', ** executable_path, headless=False)
    browser.visit(url1)
    # Use beautiful soup to parse html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Declare empty array to append to.
    latest_title = []
    latest_paragraph = []
    # Get the newest title
    title = soup.find('div', class_='content_title')
    title = title.text.strip()
    latest_title.append(title)
    # Get the newest paragraph
    paragraph = soup.find('div', class_='article_teaser_body')
    paragraph = paragraph.text.strip()
    latest_paragraph.append(paragraph)
    # Store latest article into a dictionary
    latest_news = {
        "title": latest_title,
        "paragraph": latest_paragraph
    }

    # Make a path for browser to turn into soup and scrape the featured img
    browser.visit(url4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Click on the full image button
    browser.links.find_by_partial_text('FULL IMAGE').click()
    # Select the tag with the img link and parse it into a string link.
    img = soup.find('a', class_='showimg fancybox-thumbs')
    img = str(img)
    img = "https://spaceimages-mars.com/"+img.split('"')[3]
    # Store the link into a dictionary
    featured_img = {
        "featured_img": img
    }
    # Make a path for browser to turn into soup and scrape the hemisphere titles and images
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find_all('div', class_='item')
    item = str(item)
    # Declare empty arrays to add links of images and titles
    title_list = []
    img_list = []
    # Loop through and add titles and links to the empty array
    for pic in item:
        title = ((str(pic.h3)).split("<h3>")[1])
        title = (title.split("</h3>")[0])
        title_list.append(title)
        img = "https://marshemispheres.com/"+str(pic).split('"')[11]
        img_list.append(img)
    # Store the links and titles into a dictionary
    hemispheres = {
        "titles":title_list,
        "images":img_list
    }
    # Close browser
    browser.quit()
    #Return scraped results
    return df1,latest_news,featured_img,hemispheres


# # Initialize PyMongo to work with MongoDBs
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# #Creates/Defines database in Mongo
# db = client.mars_db
# #Define tables in database
# facts = db.facts
# news = db.news
# featured = db.featured
# hemispheres = db.hemispheres
# #Creates and inserts all dataframes into their tables
# news.insert_many(latest_news.to_dict('records'))
# facts.insert_many(df1.to_dict('records'))
# featured.insert_many(featured_img.to_dict('records'))
# hemispheres.insert_many(hemispheres.to_dict('records'))