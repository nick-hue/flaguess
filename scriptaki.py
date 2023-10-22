import requests
from bs4 import BeautifulSoup

def get_image(img_name, img_url):
	with open(f'Flags/flag_{img_name}.png', 'wb') as handler:
		data = requests.get("https://www.worldometers.info"+img_url).content
		handler.write(data)

url = "https://www.worldometers.info/geography/flags-of-the-world/"
response = requests.get(url = url)
soup = BeautifulSoup(response.content, 'html.parser')

flags = soup.find_all(attrs = {"class":"col-md-4"})
flag_names = []
for flag in flags:
	flag_name = flag.find("div", attrs = {"style":"font-weight:bold; padding-top:10px"}).text
	flag_image_url = flag.div.a['href']
	

	get_image(flag_name, flag_image_url)

	if (flag_name == "Zimbabwe"):
		break

	#print(f"Name: {flag_name} | url : https://www.worldometers.info{flag_image_url}")
	flag_names.append(flag_name)
	#print(type(flag_image_url))
