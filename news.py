import requests
import json
url = "https://google-news-api1.p.rapidapi.com/search"

querystring = {"language":"EN","q":"Tech Jobs"}

headers = {
	"X-RapidAPI-Key": "2c402e092fmsh5989680423ba3d6p1ccc61jsn58bc24c9b179",
	"X-RapidAPI-Host": "google-news-api1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

with open("news.json","w") as f:
    f.write(json.dumps(response.json()))