import requests
from bs4 import BeautifulSoup

l=[]
o={}


target_url = "https://api.scrapingdog.com/scrape?api_key=642e45632aca1424a733abd3&url=https://in.indeed.com/jobs?q=fullstack&l=India&from=searchOnHP"


resp = requests.get(target_url)
print(resp.status_code)
soup = BeautifulSoup(resp.text, 'html.parser')

allData = soup.find("ul",{"class":"jobsearch-ResultsList css-0"})

alllitags = allData.find_all("div",{"class":"cardOutline"})
print(len(alllitags))
# print(alllitags)  
for i in range(0,len(alllitags)):
    try:
        o["name-of-the-job"]=alllitags[i].find("a",{"class":"jcs-JobTitle css-jspxzf eu4oa1w0"}).text
    except:
        o["name-of-the-job"]=None

    try:
        o["name-of-the-company"]=alllitags[i].find("div",{"class":"companyInfo"}).find("span",{"class":"companyName"}).text
    except:
        o["name-of-the-company"]=None


    try:
        o["rating"]=alllitags[i].find("div",{"class":"companyInfo"}).find("span",{"class":"ratingsDisplay"}).text
    except:
        o["rating"]=None

    try:
        o["salary"]=alllitags[i].find("div",{"class":"metadata salary-snippet-container"}).find("div",{"class":"attribute_snippet"}).text
    except:
        o["salary"]=None

    try:
        o["job-details"]=alllitags[i].find("div",{"class":"jcs-JobTitle css-jspxzf eu4oa1w0"}).find("div",{"class": "job-snippet"}).find("li").text
    except:
        o["job-details"]=None

    l.append(o)
    o={}


print(l)