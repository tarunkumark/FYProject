from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import json
from selenium import webdriver
import warnings
warnings.simplefilter(action='ignore',category=FutureWarning)
warnings.simplefilter(action='ignore',category=DeprecationWarning)
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
firefox_binary = FirefoxBinary("C:\Program Files\Mozilla Firefox\firefox.exe")
import re
l=list()
o={}

pages = int(input("Enter number of pages to scrape: "))
target_url = "https://www.glassdoor.com/Job/india-software-developer-jobs-SRCH_IL.0,5_IN115_KO6,24.htm?fromAge=14&seniorityType=entrylevel&includeNoSalaryJobs=true"

driver = webdriver.Firefox(firefox_binary=firefox_binary)

driver.get(target_url)
time.sleep(10)

container_xpath = "/html/body/div[2]/div/div/div/div/div[2]/section/article/div[1]/ul"




for i in range(pages):
    print("Page: ",i+1)
    container = driver.find_element("xpath",container_xpath)
    jobs = container.find_elements(By.TAG_NAME,"li")
    for job in jobs:
        i = jobs.index(job) + 1
        url_xpath = f"{container_xpath}/li[{i}]/div[2]/div[1]/a"
        company_xpath = f"{url_xpath}/span"
        job_title_xpath = f"{container_xpath}/li[{i}]/div[2]/a/span"
        location_xpath = f"{container_xpath}/li[{i}]/div[2]/div[2]/span"
        salary_xpath = f"{container_xpath}/li[{i}]/div[2]/div[3]/div[1]/span"
        url_click = job.find_element("xpath",url_xpath)
        url = url_click.get_attribute("href")
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, url_xpath)))
        actions = ActionChains(driver)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        actions.move_to_element(element).click().perform()
        driver.execute_script("arguments[0].click();", element)
        desc_xpath = '//*[@id="JobDescriptionContainer"]'
        parent_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, desc_xpath)))
        child_elements = parent_element.find_elements("xpath","./*")
        text_content = ""
        for child_element in child_elements:
            if child_element.tag_name == "ul":
                # handle ul element
                li_elements = child_element.find_elements_by_tag_name("li")
                for li_element in li_elements:
                    text_content += li_element.text
            else:
                # handle other elements
                try:
                    text_content += child_element.text
                except:
                    pass

        # define a regular expression pattern to search for
        pattern = r"(?i)\b\d+(\+|-)?\s*(years|yrs)\s+experience\b"

        # use the search() function from the re module to search for the pattern in the text content
        match = re.search(pattern, text_content)

        # check if a match was found
        if match:
            print("Experience requirement found!")
            continue
        company = job.find_element("xpath",company_xpath).text
        job_title = job.find_element("xpath",job_title_xpath).text
        try:
            location = job.find_element("xpath",location_xpath).text
        except:
            location = "NA"
        try:
            salary = job.find_element("xpath",salary_xpath).text
        except:
            salary = "NA"
        o["url"] = url
        o["company"] = company
        o["job_title"] = job_title
        o["location"] = location
        o["salary"] = salary
        o["description"] = text_content
        l.append(o)
        o={}
print(l)
with open("glassdoor.json","w") as f:
    json.dump(l,f,indent=4)
driver.close()
driver.quit()   
