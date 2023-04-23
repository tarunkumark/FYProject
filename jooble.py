import http.client
import json
host = 'jooble.org'
key = 'eab87288-b254-4642-921d-7c4f093b5eaf'

connection = http.client.HTTPConnection(host)
#request headers
headers = {"Content-type": "application/json"}
#json query
body = '{ "keywords": "software", "location": "India","Experience": "0"}'
connection.request('POST','/api/' + key, body, headers)
response = connection.getresponse()
print(response.status, response.reason)

with open("jooble.json","w") as f:
    f.write(response.read().decode('utf-8'))
print(response.read())