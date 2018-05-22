from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = "https://www.ebay.ca/sch/i.html?_odkw=24-105+canon&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR11.TRC1.A0.H0.X24-105.TRS0&_nkw=24-105&_sacat=0"

#open connection to get the page as html
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close() #close connection

#html parsing
page_soup = soup(page_html, "html.parser")

#get containters from page, containing relevant data (in this case, every camera lens)
containers = page_soup.findAll("li", {"class":"sresult lvresult clearfix li"})

#file writer
f = open("lens_info.csv", "w", encoding='utf-8')

headers = "Lens Name, Price, Shipping\n"
f.write(headers)

#for loop to extract data from every container
for container in containers:

	#get name of lens
	name = container.h3.a["title"].strip('Click this link to access')
	
	#get price
	price_contained = container.findAll("span", {"class":"bold"})
	
	#delete unnecessary child elements 
	price_unnecessary = container.find("div", {"class":"medprc"})
	price_contained[0] = str(price_contained[0]).replace(str(price_unnecessary), '')
	
	price = str(soup(price_contained[0], "html5lib").text.strip()).replace('"', '')

	#get shipping fees
	shipping_contained = container.findAll("span", {"class":"ship"})
	shipping = str(shipping_contained[0].text.strip()).replace('+', '').replace('shipping', '')
	
	f.write(name.replace(',', '') + "," + price.replace(',', '') + "," + shipping.replace(',', '') + "\n") #make sure there is no comma

f.close()


