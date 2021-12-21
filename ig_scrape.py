import csv
import time
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup

def scrape_ig(user, password, insta):
    # create browser instance
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    
    # start by booting up the main IG page
    browser.get('https://www.instagram.com/')
    time.sleep(2)

    # find the user and password boxes
    username_input = browser.find_element_by_css_selector("input[name='username']")
    password_input = browser.find_element_by_css_selector("input[name='password']")

    # input username and password
    username_input.send_keys(user)
    password_input.send_keys(password)

    # find the login button then click
    login_button = browser.find_element_by_xpath("//button[@type='submit']")
    login_button.click()

    # wait for 10 seconds so we have time for the page to load
    time.sleep(10)

    # jump to page to scrape, skip the notification prompt
    browser.get('https://www.instagram.com/' + insta)

    # scroll down 3 times
    num_scrolls = 3
    while(num_scrolls > 0):
        scrolldown = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        time.sleep(3)
        num_scrolls -= 1

    # save the page html in case we need something for later
    html = browser.page_source
    
    # collect all links to posts
    posts = []
    links = browser.find_elements_by_tag_name("a")
    for link in links:
        post = link.get_attribute("href")
        if "/p/" in post:
            posts.append(post)
        
    # download image from latest post only
    target = posts[0]

    # load the latest post
    browser.get(target)

    # find the image from the post
    res = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div/div[1]/div/div/div[1]/img')
    
    # get the src of the image then download it as sample.jpg
    if res is not None:
        dl_url = res.get_attribute("srcset")
        dl = dl_url.split(" ")[0]
        urllib.request.urlretrieve(dl, "sample.jpg")

    # wait for 10 seconds to let the download finish
    time.sleep(10)

    # close the browser
    browser.close()
    
    # pass the html to beautifulsoup to get some data
    soup = BeautifulSoup(html)
    title = soup('title')[0].text
    description = soup.find('meta', {'property': 'og:description'}).attrs['content']

    return title, description, posts


if __name__ == '__main__':
    # User and password is required, but I redacted it from the code
    USER = ""
    PASSWORD = ""
    insta = "theoatmeal"
    
    title, description, posts = scrape_ig(user=USER, password=PASSWORD, insta=insta)
    
    # save scraped details to a csv file
    with open('IG_Parsing.csv', mode='w', newline='') as ig_csv:
        ig_writer = csv.writer(ig_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        ig_writer.writerow(['Instagram Link', 'https://www.instagram.com/' + insta])
        ig_writer.writerow(['Title', title])
        ig_writer.writerow(['Description', description])
        ig_writer.writerow(['Link to posts:'])
        ig_writer.writerows([[post] for post in posts])
    