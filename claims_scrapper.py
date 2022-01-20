import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# modificar código para incluir lugar, fecha, título y objetivo?

PATH = '/Users/stino/Desktop/scrape/chromedriver'
service = Service(PATH)

# options to avoid cloudflare
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service = service, options = options)

# add the companies to scrape
print("Please enter the companies to scrape (separate by '_' in case of name of many words):")
companies = input()
companies = companies.split(' ')
companies = [i.title().replace('_', ' ') for i in companies]

claims = pd.DataFrame()
for company in companies:
    driver.get('https://www.reclamos.cl')

    # search by company
    search = driver.find_element(By.NAME, 'concepto')
    search.send_keys(company)
    search.send_keys(Keys.RETURN)

    # click on summary
    claims_redirect = driver.find_element(By.XPATH, '//*[@id="container-main"]/div[1]/div/div/a[1]')
    claims_redirect.click()

    corpus = []
    while True:
        # access the claims on the table
        base_link = driver.current_url # link of webpage containing the table
        table = driver.find_element(By.XPATH, '//*[@id="container-main"]/div[1]/div[2]/div/div[2]/table') # select table with urls
        table_links = [link.get_attribute('href') for link in table.find_elements(By.TAG_NAME, 'a')] # get urls
        for link in range(len(table_links)): # loop through the rows in the table
            driver.get(table_links[link]) # navigate to the url
            text = driver.find_element(By.CLASS_NAME, "reclamo-texto-principal") # get the claim
            corpus.append(text.get_attribute('innerHTML')) # store the claim

        # advance to the next page
        driver.get(base_link)
        try: 
            next = driver.find_element(By.XPATH, "//a[@title='Ir a la página siguiente']")
            next.click()
        except: 
            break # break if 'next_page' not found

    claims_tmp = pd.DataFrame({'corpus': corpus}) # generate a temporary dataframe
    claims_tmp['company'] = company # create a column with the company
    claims = claims.append(claims_tmp) # append claims

claims.to_csv('claims.csv', encoding = 'utf-8-sig', sep = ';', index = False)

driver.quit() # close the browser