import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import numpy as np

def scrape_data():
    # Declare empty list to append dictionaries to
    data_list = []
    # Declare data sources
    url1 = "https://redplanetscience.com"
    url2 = "https://galaxyfacts-mars.com/"
    url3 = "https://marshemispheres.com/"
    url4 = "https://spaceimages-mars.com/"
    # Make a table full of facts from earth and mars
    tables = pd.read_html(url2)
    df = tables[0]
    # df_dict = df.to_dict('records')
    df_dict = {"category":(df[0].to_list()),"mars":(df[1].to_list()),"earth":(df[2].to_list())}
    # Add the newly scraped table to 
    data_list.append(df_dict)
    # Make a path for browser to visit and scrape data from latest news article
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', ** executable_path, headless=False)
    browser.visit(url1)
    # Use beautiful soup to parse html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Get the newest title
    title = soup.find('div', class_='content_title')
    title = title.text.strip()
    # Get the newest paragraph
    paragraph = soup.find('div', class_='article_teaser_body')
    paragraph = paragraph.text.strip()
    # Store latest article into a dictionary
    latest_news = {
        "title": title,
        "paragraph": paragraph
    }
    # Append dictionary to list
    data_list.append(latest_news)
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
    # Append dictionary to list
    data_list.append(featured_img)
    # Make a path for browser to turn into soup and scrape the hemisphere titles and images
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find_all('div', class_='item')
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
    # Append dictionary to list
    data_list.append(hemispheres)
    # Close browser
    browser.quit()
    #Return scraped results
    return data_list