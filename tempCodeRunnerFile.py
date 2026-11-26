import requests
url = "https://api.mymemory.translated.net/get"

params = {
    "q" : "hello",
    "langpair" : "en|ur"
}

response = requests.get(url, params=params)
print(response.status_code)

data = response.json()

print(data["responseData"]["translatedText"])
