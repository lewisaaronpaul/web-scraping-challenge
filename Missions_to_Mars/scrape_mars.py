# Import modules
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import time
import json
import os
import pandas as pd

# Selenium modules
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#chrome_path = 'C:\WebDrivers\chromedriver.exe'


def init_browser():
    # @NOTE: Path to the chromedriver.
    chrome_path = 'C:\WebDrivers\chromedriver.exe'
    return webdriver.Chrome(chrome_path)


def scrape():
    # Run Google Chrome from Python.
    driver = init_browser()

    # Create mars_dict to collect the information along the way:
    mars_dict = {}
       
    #########################################################################
    # NASA Mars News
    #########################################################################

    # Open the webpage from Python.
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    driver.get(url)

    time.sleep(15)

    # Get the HTML for the website.
    html = driver.execute_script('return document.documentElement.outerHTML')

    #Close the driver
    #driver.close()

    # This is the HTML for the webpage
    soup = BeautifulSoup(html, 'lxml')
    page = soup.find('div', id = 'page')

    # Find all <li> tags
    all_lis = [li for li in page.ul.find_all('li')]

    # The latest news is in the first <li> tag.
    latest_li = all_lis[0]

    latest_news_title = latest_li.find('div', class_ = 'content_title').text
    latest_news_p = latest_li.find('div', class_ = 'article_teaser_body').text

    # latest news title and paragraph
    mars_dict["latest_news_title"] = latest_news_title
    mars_dict["latest_news_p"] = latest_news_p

    ###################################################################################
    # JPL Mars Space Images - Featured Image
    ###################################################################################

    # Run Google Chrome from Python.
    url_JPL_Mars = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #driver = webdriver.Chrome(chrome_path)
    driver.get(url_JPL_Mars)

    # Get the HTML of the current page you are on.
    image_html = driver.page_source

    # This is the HTML for the webpage
    image_soup = BeautifulSoup(image_html, 'lxml')

    # Search for the tag of the full image, using link text.
    image_link = driver.find_element_by_link_text('FULL IMAGE')

    # Click on the link for the full image.
    image_link.click()

    # Wait for conpletion of previous action.
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.LINK_TEXT, "more info"))
        )
        
        # Click on the button for more info.
        element.click()
    except:
        driver.quit()

    # Get the HTML of the current page for the large picture.
    large_html = driver.page_source

    #Close the driver
    #driver.close()

    # This is the HTML for the full picture webpage
    large_soup = BeautifulSoup(large_html, 'lxml')

    figure_tag = large_soup.find('figure', class_ = 'lede')
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url+figure_tag.a['href']

    mars_dict["featured_image_url"] = featured_image_url

    ############################################################################
    # Mars Weather
    ############################################################################

    # Run Google Chrome from Python.
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    #driver = webdriver.Chrome(chrome_path)
    driver.get(url_weather)

    time.sleep(15)

    # Get the HTML of the current page you are on.
    weather_html = driver.page_source

    #Close the driver
    #driver.close()

    # This is the HTML for the Twitter webpage on Mars weather.
    weather_soup = BeautifulSoup(weather_html, 'lxml')

    div_tag = weather_soup.find('div', class_ = 'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    mars_weather = div_tag.text

    mars_dict["mars_weather"] = mars_weather

    #######################################################################
    # Mars Facts
    #######################################################################

    # Fetch the page at the url using "requests" module.
    facts_url = 'https://space-facts.com/mars/'
    response = requests.get(facts_url)

    time.sleep(15)

    # Read all tables in the response into a list of dataframes
    dfs=pd.read_html(response.text)

    # Iterate through the DataFrames to access each table.
    facts_df = dfs[0]
    facts_df.columns = ['variable', 'value']
    facts = facts_df.set_index('variable')

    # Save DataFrame as HTML.
    facts_html_path = os.path.join(".", "facts.html")
    facts.to_html(facts_html_path, encoding="utf-8", index=True)

    mars_df = facts.T
    mars_df.columns = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons',
        'Orbit Distance', 'Orbit Period', 'Surface Temperature',
        'First Record', 'Recorded By']

    # Save DataFrame as HTML.
    mars_html_path = os.path.join(".", "mars_facts.html")
    mars_df.to_html(mars_html_path, encoding="utf-8", index=False)

    #####################################################################
    # Mars Hemispheres
    #####################################################################

    # Run Google Chrome from Python.
    url_hemis = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #driver = webdriver.Chrome(chrome_path)
    driver.get(url_hemis)

    time.sleep(15)

    hemisphere_image_urls = []
    #########################################################################

    # Cerberus Hemisphere

    # Search for the tag of the full image, using link text.
    cerberus_link = driver.find_element_by_link_text('Cerberus Hemisphere Enhanced')

    # Click on the link for the full image.
    cerberus_link.click()

    # Get the HTML of the current page.
    cerberus_hemis_html = driver.page_source

    # This is the HTML for the full picture webpage
    cerberus_soup = BeautifulSoup(cerberus_hemis_html, 'lxml')

    cerberus_title = cerberus_soup.find('h2', class_ = 'title').text[:-9]

    mars_dict["cerberus_title"] = cerberus_title

    cerberus_div_img = cerberus_soup.find('div', class_ = 'downloads')
    cerberus_img_url = cerberus_div_img.a['href']

    mars_dict["cerberus_img_url"] = cerberus_img_url

    # Dictionary
    cerberus_dict = {}
    cerberus_dict['title'] = cerberus_title
    cerberus_dict['img_url'] = cerberus_img_url

    hemisphere_image_urls.append(cerberus_dict)

    driver.back()
    ######################################################################

    # Schiaparelli Hemisphere

    # Search for the tag.
    schiaparelli_link = driver.find_element_by_link_text('Schiaparelli Hemisphere Enhanced')

    # Click on the link.
    schiaparelli_link.click()

    # Get the HTML of the current page.
    schiaparelli_html = driver.page_source

    # This is the HTML for the current webpage
    schiaparelli_soup = BeautifulSoup(schiaparelli_html, 'lxml')

    schiaparelli_title = schiaparelli_soup.find('h2', class_ = 'title').text[:-9]

    mars_dict["schiaparelli_title"] = schiaparelli_title

    schiaparelli_div_img = schiaparelli_soup.find('div', class_ = 'downloads')
    schiaparelli_img_url = schiaparelli_div_img.a['href']

    mars_dict["schiaparelli_img_url"] = schiaparelli_img_url

    # Dictionary
    schiaparelli_dict = {}
    schiaparelli_dict['title'] = schiaparelli_title
    schiaparelli_dict['img_url'] = schiaparelli_img_url

    hemisphere_image_urls.append(schiaparelli_dict)

    driver.back()
    #########################################################################

    # Syrtis Major Hemisphere

    # Search for the tag.
    syrtis_link = driver.find_element_by_link_text('Syrtis Major Hemisphere Enhanced')

    # Click on the link.
    syrtis_link.click()

    # Get the HTML of the current page.
    syrtis_html = driver.page_source

    # This is the HTML for the current webpage
    syrtis_soup = BeautifulSoup(syrtis_html, 'lxml')

    syrtis_title = syrtis_soup.find('h2', class_ = 'title').text[:-9]

    mars_dict["syrtis_title"] = syrtis_title

    syrtis_div_img = syrtis_soup.find('div', class_ = 'downloads')
    syrtis_img_url = syrtis_div_img.a['href']

    mars_dict["syrtis_img_url"] = syrtis_img_url

    # Dictionary
    syrtis_dict = {}
    syrtis_dict['title'] = syrtis_title
    syrtis_dict['img_url'] = syrtis_img_url

    hemisphere_image_urls.append(syrtis_dict)

    driver.back()
    ##################################################################

    # Valles Marineris Hemisphere Enhanced

    # Search for the tag.
    valles_link = driver.find_element_by_link_text('Valles Marineris Hemisphere Enhanced')

    # Click on the link.
    valles_link.click()

    # Get the HTML of the current page.
    valles_html = driver.page_source

    # This is the HTML for the current webpage
    valles_soup = BeautifulSoup(valles_html, 'lxml')

    valles_title = valles_soup.find('h2', class_ = 'title').text[:-9]

    mars_dict["valles_title"] = valles_title

    valles_div_img = valles_soup.find('div', class_ = 'downloads')
    valles_img_url = valles_div_img.a['href']

    mars_dict["valles_img_url"] = valles_img_url

    # Dictionary
    valles_dict = {}
    valles_dict['title'] = valles_title
    valles_dict['img_url'] = valles_img_url

    hemisphere_image_urls.append(valles_dict)

    driver.back()

    #Close the driver
    driver.close()

    return mars_dict

