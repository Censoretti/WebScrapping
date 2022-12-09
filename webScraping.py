from email import header
from attr import Attribute
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
	'Accept-Language': 'en-US, en;q=0.5'
}

searchQuery = (input('Enter the product you want to scrap: ')).replace(' ', '+')
baseUrl = 'https://www.amazon.com/s?k={0}'.format(searchQuery)

items = []

while True:
	try: 
		pageScraping = int(input('Enter how many pages you want to scrap: '))
		pageScraping += 1
	except ValueError:
		print('Not a valid number')
	else:
		break

testPrice = input('Do you want items without price? (S/N)')
if testPrice == 'S' or testPrice == 's' :
	priceLess = True
elif testPrice == 'N' or testPrice == 'n':
	priceLess = False
	

for i in range(1, pageScraping):
	response = requests.get(baseUrl + '&page={0}'.format(i), headers=headers)
	soup = BeautifulSoup(response.content, 'html.parser')

	results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

	for result in results:
		productName = result.h2.text
		try:
			price1 = (result.find('span', {'class': 'a-price-whole'}).text).replace(',','')
			price2 = result.find('span', {'class': 'a-price-fraction'}).text
			price = float(price1 + price2)
			items.append([productName, price])
		except AttributeError:
			if priceLess:
				price = 'No price'
				items.append([productName, price])
			else:
				continue
sleep(2)

df = pd.DataFrame(items, columns=['Product name', 'Price'])
df.to_csv('{0}.csv'.format(searchQuery), index=False)