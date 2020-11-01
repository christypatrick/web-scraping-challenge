#BeautifulSoup, Pandas, and Requests/Splinter
from bs4 import BeautifulSoup as soup
from splinter import Browser
import pandas as pd
import requests
import time

def init_browser():
    # Windows Users
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    # Initiate headless driver for deployment
    #browser = Browser("chrome", executable_path="chromedriver", headless=True)
    browser = init_browser()
         
    # NASA Mars News
    # URL to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    newssoup = soup(html, 'html.parser')
    
    slide_elem = newssoup.select_one('ul.item_list li.slide')

    # Use the parent element to find the first tag and save it as `news_title`
    news_title = slide_elem.find("div", class_='content_title').get_text()
    news_title

    # Use the parent element to find the first tag and save it as `news_title`
    news_p = slide_elem.find("div", class_='article_teaser_body').get_text()
    news_p

    # JPL Mars Space Images - Featured Image
    # define URL to scrape and inform browser to visit the page 
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    #Click full image
    browser.click_link_by_partial_text('FULL IMAGE')

    #click more info
    browser.click_link_by_partial_text('more info')

    time.sleep(1)

    html= browser.html
    jplsoup = soup(html, 'html.parser')

    # pull images from site
    image_url = jplsoup.find('img', class_='main_image').get('src')

    # full image URL
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url
    
    # Mars Facts

    # define URL to scrape and inform browser to visit the page - do this for every url
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    #scrape the table containing facts about the planet including Diameter, Mass, etc.
    #automatically scrape the tabular data from the page
    tables = pd.read_html(facts_url)

    # select the Mars Planet Profile table
    table_df = tables[0]
    #table_df

    # assign columns and set index of dataframe
    table_df.columns = ['Description', 'Mars']
    table_df.set_index('Description', inplace=True)

    #Use Pandas to convert the data to a HTML table string
    html_table = table_df.to_html(classes="table table-striped")

    # Mars Hemispheres

    # define URL to scrape and inform browser to visit the page - do this for every url
    # USGS Astrogeology site
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)

    # Store prefix for URL
    url_prefix = 'https://astrogeology.usgs.gov'


    #click each of the links to the hemispheres in order to find the image url to the full resolution image
    #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title 
    #containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.

    # Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
    html = browser.html
    marssoup = soup(html, 'html.parser')

    # Retreive all items that contain hemisphere info
    hem_item = marssoup.findAll('div', class_='item')

    # Empty list for hemisphere urls 
    hem_image_url = []

    for x in hem_item:
            
        # Store title
        title = x.find('h3').text
        
        # Store link
        h_img_url = x.find('a', class_='itemLink product-item').get('href')
        
        # Visit link that contains the full image
        browser.visit(url_prefix + h_img_url)
        
        # HTML Object and beaautiful soup
        html = browser.html    
        hem_soup = soup(html, 'html.parser')
        
        # Retrieve full image source 
        img_url = url_prefix + hem_soup.find('img', class_='wide-image').get('src')
        
        #Append the dictionary with the image url string and the hemisphere title to a list. 
        #This list will contain one dictionary for each hemisphere.
        hem_image_url.append({"title" : title, "img_url" : img_url})

    hem_image_url    

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "html_table": html_table,
        "hem_image_url": hem_image_url 
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict

