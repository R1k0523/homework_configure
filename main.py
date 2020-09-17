import requests
from lxml import html
import urllib

def get_link(package_name):
    url = "https://pypi.org/simple/"+package_name
    response = requests.get(url)
    if (response.status_code == 200):
        body = html.fromstring(response.text)
        return (body.xpath('//a/@href')[-1])
    return 'No suck package'

r = requests.get(get_link("django"), allow_redirects=True)
open('archive.zip', 'wb').write(r.content)