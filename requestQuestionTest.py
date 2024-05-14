import requests
from bs4 import BeautifulSoup

import WriteFile
# 奥数库基础网址
rootUrl = "https://www.aoshuku.com/"

requestObj = requests.get(rootUrl)

soup = BeautifulSoup(requestObj.content)
print(soup.prettify)

netContent = soup.decode()

WriteFile.writeContent2File(netContent, "./", "aushuku", "json")