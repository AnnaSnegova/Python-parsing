import urllib.request as url
import json
from bs4 import BeautifulSoup
import requests
import lxml

URL = "https://grid.ac"
url_part1 = "/institutes/"
url_part2 = '?page=1'
url_all = URL+url_part1+url_part2




def get_html(url_all):
	r = requests.get(url_all)
	return r.text

def get_json(html):
	

	soup = BeautifulSoup(html, 'lxml')
	get_adress = soup.find('h4', class_='name')
	adress = URL + get_adress.find('a').get('href')+'.json'
	



	request = url.Request(
    adress,
headers={
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
	
	response = url.build_opener(url.HTTPCookieProcessor()).open(request)
	data = json.loads(response.read().decode('utf-8'))
	
	

	
# ниже переводим json в вывод html файла. Сдохнуть можно.

	output = []
	for row in data['institute']['name']:

		

		result = ("<div style='padding: 20px, background: #аааа'>"
	 
	 			"<h1>{}</h1>"
				"</div>"
				"<br />"
				"<hr />"
				"<br />"
				).format(
		row['0'] or '' if '0' in row else '',
			# row['0'] or '' if '0' in row else '',
		# row[] or '' if  in row else '',
		
			# row['id'] or '' if 'id' in row else '',
	# 	#                     # row['selftext'] or '' if 'selftext' in row else '',
 	                )
		output.append(result)
		
		

# Вывод собранного массива строк (output) в файл .html
	with open('view.html', 'w', encoding='utf-8') as f:
		f.write( '\n<br>\n'.join(output) )








def main():
	get_json(get_html(url_all))




if __name__ == '__main__':
	main()
 







