import requests
from bs4 import BeautifulSoup
search = ''
url = 'https://tw.op.gg/champion/statistics#'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
item = soup.find_all('div',{'class':'champion-index-table__name'})
print(item[0].text)