import urllib.request as url
import json
from bs4 import BeautifulSoup
import requests
import lxml


class Parser:
	data           = []
	target_domain  = ""
	target_path    = ""
	headers        = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
	}

	def fetch(self, request={}):
		raise NotImplementedError()

	def get_json(self, address, headers=None):
		headers = self.headers if headers == None else headers
		request = url.Request(address, headers=headers)
		response = url.build_opener(url.HTTPCookieProcessor()).open(request)
		return json.loads(response.read().decode('utf-8'))

	def generate_html(self):
		raise NotImplementedError()

	def get_target(self, request={}, path=None):
		path = self.target_path if path == None else path
		if type(request) != dict:
			raise ValueError()

		# request = {'page': 5}
		target_request = []
		for k, v in request.items():
			target_request.append('{}={}'.format(k, v))

		return "https://{}/{}?{}".format(
				self.target_domain, path,
				'&'.join(target_request),
			)


class GridParser(Parser):
	target_domain  = "grid.ac"
	target_path    = "institutes/"

	def fetch(self, request={'page':1}):
		url = self.get_target(request)
		print('Requesting ', url, ' ...')
		html = requests.get(url).text
		soup = BeautifulSoup(html, 'lxml')
		addresses = soup.find_all('h4', class_='name')

		self.data = []
		for l in addresses:
			address = self.get_target(path=l.find('a').get('href') + '.json')
			print('Request: ', address)
			self.data.append( self.get_json(address) )
		return self

	def generate_html(self):
		print('HTML generating...')
		output = []
		for row in self.data:
			institute = row['institute']
			result = ("<div style='padding: 20px, background: #аааа'>"
		 			  "<h1>{}</h1>"
		 			  "<a href='{}'>Link</a>"
					  "</div>"
					  "<br />"
					  "<hr />"
					  "<br />"
					).format(
						institute['name'] or ''
							if 'name' in institute else 'Noname',
						institute['links'][0] or ''
							if 'links' in institute and len(institute['links']) > 0 else '',
	 	            )
			output.append(result)
		return '\n<br>\n'.join(output)


# class RedditParser():
# 	pass