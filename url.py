import requests

url = "https://kvantomat24.serveo.net"
def met(new_url, urls):
    global url
    if requests.get("https://github.com/"):
        url = new_url
    return url

url=met("adad", url)
print(url)