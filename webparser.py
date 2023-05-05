# import requests
# from bs4 import BeautifulSoup

# url = 'https://in.indeed.com/jobs?q=Software&l=India&from=searchOnHP&vjk=7ae02d295dd3ce50'

# # Send a request to the URL and get the HTML content
# response = requests.get(url)
# html_content = response.content

# # Create a BeautifulSoup object and parse the HTML content
# soup = BeautifulSoup(html_content, 'html.parser')

# # Find all the job postings on the page
# job_postings = soup.find_all()
# print(len(job_postings))
# # Loop through each job posting and extract the job title and URL
# for job_posting in job_postings:
#     # Extract the job title
#     job_title_element = job_posting.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')
#     job_title = job_title_element.text.strip()

#     # Extract the job URL
#     job_url = 'https://in.indeed.com' + job_title_element['href']

#     print(job_title)
#     print(job_url)



# # jobTitle css-1h4a4n5 eu4oa1w0
# import requests
# from bs4 import BeautifulSoup

# URL = "https://www.naukri.com/full-stack-developer-jobs?src=popular_roles_homepage_srch&experience=0"
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}    
# response = requests.get(URL, headers=headers).content
# with open('indeed.html', 'wb') as f:
#     f.write(response)
#     f.close()
# print(response)
# soup = BeautifulSoup(response, 'html.parser')

# results = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})

# for x in results:

#     company = x.find('span', attrs={"class":"company"})
#     if company:
#         print('company:', company.text.strip() )

#     job = x.find('a', attrs={'data-tn-element': "jobTitle"})
#     if job:
#         print('job:', job.text.strip())

#     salary = x.find('nobr')
#     if salary:
#         print('salary:', salary.text.strip())

#     print ('----------')

import pandas as pd
import time
from bs4 import BeautifulSoup
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
pages = int(input('Enter number of pages to scrape: '))
page = 0
df = pd.DataFrame(columns=['title','company','ratings','reviews','experience',
                           'salary','location','tags','url'])

url = "https://www.naukri.com/frontend-jobs-in-india?k=frontend&l=india&nignbevent_src=jobsearchDeskGNB&experience=0&jobAge=15"
driver = webdriver.Firefox(firefox_binary=firefox_binary)
driver.get(url)
action = ActionChains(driver)
for i in range(1,pages+1):
        # insert link to 2nd page here, replace number 2 with str(i)
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/section[2]/div[3]/div/a[2]")))
    # element.click()
    actions = ActionChains(driver)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
# move the mouse to the element and click it
    # actions.move_to_element(element).click().perform()
    driver.execute_script("arguments[0].click();", element)
    time.sleep(4)
    
    soup = BeautifulSoup(driver.page_source,'html5lib')
    
    # driver.close()
    
    results = soup.find(class_="list")
    job_elems = results.find_all('article',class_='jobTuple')
    
    for job_elem in job_elems:

        # Job URL
        url = job_elem.find('a',class_='title ellipsis').get('href')

        # Job Title
        title = job_elem.find('a',class_='title ellipsis')

        # Number of reviews
        review_span = job_elem.find('a',class_='reviewsCount fleft')
        if review_span is None:
            continue
        else:
            reviews = review_span.text

        # Company ratings
        rating_span = job_elem.find('span',class_='starRating fleft')
        if rating_span is None:
            continue
        else:
            ratings = rating_span.text

        # Company name
        company = job_elem.find('a',class_='subTitle ellipsis fleft')

        # Experience required
        Exp = job_elem.find('li',class_='fleft br2 placeHolderLi experience')
        if Exp is None:
            continue
        else:
            Exp_span = Exp.find('span',class_='ellipsis fleft expwdth')
            Experience = Exp_span.text

        # Salary
        Sal = job_elem.find('li',class_='fleft br2 placeHolderLi salary')
        Sal_span = Sal.find('span',class_='ellipsis fleft')
        if Sal_span is None:
            continue
        else:
            Salary = Sal_span.text

        # Location
        Loc = job_elem.find('li',class_='fleft br2 placeHolderLi location')
        Loc_exp = Loc.find('span',class_='ellipsis fleft locWdth')
        if Loc_exp is None:
            continue
        else:
            Location = Loc_exp.text

        # Days since job was posted
        # hist = job_elem.find('div', class_='jobTupleFooter mt-8')
        # hist2 = hist.find('div', class_='tupleTagsContainer')
        # hist3 = hist2.find('span', class_='fleft postedDate')
        
        # job Tags
        tags = job_elem.find('ul',class_='tags has-description')
        tag1 = ""
        for tag in tags:
            tag1 += " "+tag.text

        # Adding data to dataframe
        df = df.append({'title':title.text,'company':company.text,'ratings':ratings,
                'reviews':reviews,'experience':Experience,'salary':Salary,
                'location':Location,'tags':tag1,'url':url}, 
                 ignore_index=True)
    
        
    page += 1
    print(f'Pages done {page}/{pages}')
    
df.duplicated().sum()

df2 = df.drop_duplicates()

df2.to_csv('data/naukri_scraped_data.csv', index=None)