# # Web Scraping Homework - Mission to Mars
# In this assignment, you will build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.


# Dependencies
from bs4 import BeautifulSoup
import requests


# ## Step 1 - Scraping

# #### NASA Mars News
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later



# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# Retrieve page with the requests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
soup = BeautifulSoup(response.text, 'lxml')




# Examine the results, then determine element that contains sought info
print(soup.prettify())



# results are returned as an iterable list
results = soup.find('div', class_='slide')

# Identify and return title of article
news_title = results.find('div', class_='content_title').text
# Identify and return article teaser
news_p = results.find('div', class_='rollover_description_inner').text
 
print(f'{news_title} {news_p}')


# #### JPL Mars Space Images - Featured Image
# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`



from splinter import Browser
import time




executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)



#visit url
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)




#https://blog.scrapinghub.com/2016/10/27/an-introduction-to-xpath-with-examples
xpath = "//section[1]/div/div/article/div[1]/footer"

#Click 'full image' button then pause for 2 seconds
results = browser.find_by_xpath(xpath)
button = results[0]
button.click()
time.sleep(2)




#Parse featured image's 'src'
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
img_url = soup.find('div', class_='fancybox-wrap').img['src']

#Create full image url
featured_img_url = f"https://www.jpl.nasa.gov/{img_url}"
print(featured_img_url)


# #### Mars Weather



#Retrieve html
url = 'https://twitter.com/marswxreport?lang=en' 
response = requests.get(url) 
results = BeautifulSoup(response.text, 'html.parser')
results




#Parse 1st tweet's text
tweet = results.find('div',class_='js-tweet-text-container').p.text
print(tweet)


# #### Mars Facts



import pandas as pd
url = 'https://space-facts.com/mars/'

#create dataframe add column headers
table_df = pd.read_html(url)[0]
table_df.columns = ['Description','Value']
table_df.set_index(['Description'], inplace=True)
print(table_df)




#Create html table from df
fact_table = table_df.to_html('fact_table.html')


# #### Mars Hemispheres



#Create empty list to hold hemispher info
hemispheres = []




x=1
hemis = 4

while (x <= hemis):
    #Visit hemisphere home page 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    #Click Xth hemisphere's link
    xpath = f"//section[1]/div/div[2]/div[{x}]/div/a"
    results = browser.find_by_xpath(xpath)
    link = results[0]
    link.click()
    #Parse Xth hemisphere's html page for title
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('section', class_='block').h2.text
    title

    #Click Xth hemisphere's image
    xpath = '//div/div/ul/li[1]/a'
    results = browser.find_by_xpath(xpath)
    img_link = results[0]
    img_link.click()
    #Parse Xth hemisphere's image page for 'src' and create full url
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find('div', class_='downloads').img['src']
    img_url = f"https://astrogeology.usgs.gov/{img_url}"
    
    #Place 'title' and full 'img_url' into dict
    hemi_dict = {"title":title, 
                "img_url": img_url}
    #Append dict to hemisphere list
    hemispheres.append(hemi_dict)
    
    #Add 1 to hemisphere iterator
    x = x + 1




#Print hemispher list of dicts
print(hemispheres)






