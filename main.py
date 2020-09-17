import requests
from lxml import html


def get_link(package_name):
    url = "https://pypi.org/simple/"+package_name
    response = requests.get(url)
    if (response.status_code == 200):
        body = html.fromstring(response.text)
        return (body.xpath('//a/@href')[-1])
    return 'No suck package'



f=open(r'D:\file_bdseo.zip',"wb") #окрываем файл для записи, в режиме wb

f.write(get_link().content)