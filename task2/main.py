from myparser import GridParser

def main():
	parsed_data = GridParser().fetch({'page': 5}).generate_html()

	# Вывод данные в файл .html
	with open('view.html', 'w', encoding='utf-8') as f:
		f.write(parsed_data)


if __name__ == '__main__':
	main()
 