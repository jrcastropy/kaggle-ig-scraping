'''
Test Scraping
Kaggle Scraping using selenium's xpath
'''

from webdriver_manager.chrome   import ChromeDriverManager
from selenium                   import webdriver
from bs4                        import BeautifulSoup

import pandas as pd
import time

def main():
    driver_path = ChromeDriverManager().install()
    driver      = webdriver.Chrome(driver_path)

    kaggle_url1 = "https://www.kaggle.com/competitions"

    counter     = 1
    comp_dict   = {}

    while True:
        kaggle_url2 = f"?page={counter}"
        if counter == 1:
            kaggle_url = kaggle_url1
        else:
            kaggle_url = kaggle_url1 + kaggle_url2
        driver.get(kaggle_url)
        if counter == 1:
            driver.find_element_by_xpath("//*[@id=\"site-content\"]/div[4]/div[4]/div/div[2]/div/button[1]").click()
        time.sleep(1)
        html = driver.find_element_by_xpath("//*[@id=\"site-content\"]/div[4]/div[5]/div/div/ul").get_attribute('innerHTML')
        soup = BeautifulSoup(html)
        
        if len(soup.find_all('div')) > 2:
            for idx, li in enumerate(soup.find_all('li')):
                page_num = f"{counter}_{idx+1}"
                comp_dict[page_num] = {}
                comp_title  = li.div.find_all('div')[1].div.text
                comp_desc   = li.div.span.text
                comp_dict[page_num]['title'] = comp_title 
                comp_dict[page_num]['desc'] = comp_desc
        else:
            break
        
        counter += 1
        
    df = pd.DataFrame(comp_dict).T
    df = df.dropna()
    df.to_csv('results.csv')

if __name__ == '__main__':
    main()