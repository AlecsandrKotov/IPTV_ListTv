 # Скачиваем список канала с сайта http://proxytv.ru
import requests
from bs4 import BeautifulSoup
import os
import sys 

folder = "tv list"												#папка  для сохранения
folder_patch = './' + str(folder) + '/'							#путь папки для функции сохранения плейлиста
REQUEST_STATUS_CODE = 200										#константа запроса к сайту с ответом 200 (для проверки доступа к ресурсу)
list_url_name = []												#список ссылок и имя каналов

header = {'Host':'proxytv.ru',
		'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
		'Accept':'*/*',
		'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding':'gzip, deflate',
		'Referer':'http://proxytv.ru/index.php/poisk.html',
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'X-Requested-With':'XMLHttpRequest',
		'Content-Length':'46',
		'Connection':'keep-alive',
		'Cookie':'BL_D_PROV=undefined; BL_T_PROV=undefined; _ym_uid=1545429092523198842; _ym_d=1545429092; _ga=GA1.2.148980462.1545429094; addba227a8e1d5245ea77eca79c68301=cf29260cdd6ecb5d9966728e5c338b7c; BL_D_PROV=undefined; BL_T_PROV=undefined',
		'Pragma':'no-cache',
		'Cache-Control':'no-cache'
		}

#функция считывания файла для создания списка ссылок и названий файлов для парсинка
def open_list():
	f = open('./list_pl.txt', 'r', encoding="utf-8")
	text = f.read()
	f.close()
	text_list = text.split(',')  													#разделяем строку по запятой (получаем список)
	for tex in text_list:
		chanel = tex.strip()														#канал из списка
		get_find = 'pl:' + str(chanel).lower() 										#Запрос  к сайту по поиску канала
		folder_patch = './' + str(folder) + '/'										#путь к папке для сохранения плейлистов
		file_name = chanel+".m3u"													#Имя файла плейлиста 

		my_date = {'udpxyaddr': get_find}

		url_site = 'http://proxytv.ru/iptv/php/srch.php' 							#сайт с которого парсим список каналов
		list_url_name.append((url_site,file_name,my_date))							#список с сылками и названиями плейлистов с расширением m3u 
	#print(list_url_name)															#вывод  списка ДЛЯ ТЕСТА
	
#функция создания папки если она отсутствует
def folder_write():
	if not os.path.isdir(folder): 													#проверяем существование папки
		os.mkdir(folder)															#если папки нет создаем ее
		print ('Папка "' + folder + '" успешно создана')							#выводим информацию о успешном создании папки
	else:
		print ('Папка "' + folder + '" уже существует')

def find_to_save():
	#os.system('cls' if os.name=='nt' else 'clear')									#очищаем консоль для win и lin
	for url in list_url_name:
		url_site = url[0]															#берем из списка ссылку с запросом поска (пример запроса: ?udpxyaddr=ch:discovery)
		file_name = url[1]
		my_date = url[2]															#берем из списка имя файла плейлиста для сохранения (пример: discovery.m3u)
		#file_name_text = file_name[:file_name.find('.')]							#обрезаем имя канала без '.m3u'
		#print (my_date)

		list_http = [] 																#Пустой список данных для сохранения в файл плейлиста
		list_http.append ('#EXTM3U list-autor="© http://ProxyTV.ru"')				#Директива определяет содержимое как плейлист в формате M3U, должна быть первой значимой строкой в плейлисте.
		try:
			response = requests.post(url_site, headers=header, data=my_date)
			html = response.content


			soup = BeautifulSoup(html, 'lxml')
			div = soup.find_all('div', align="left")
																					
			if not div:																#если не находим тег ('div' align="left") останавливаем работу скрипта
				print('По запросу: "' + str(url[2]) + '" поиск результата не дал.')
				#sys.exit() 														#останавливаем работу скрипта
			else:
				if response.status_code == REQUEST_STATUS_CODE:
					#print('Соединение с сайтом установленно.')
					#print('Ждиде, идет поиск...')
					print('Создаю плейлист: ' + file_name)

					for i in div:
						line_text = i.text.strip()
						if  not line_text.find('#'):
							line_split = line_text.rfind('#')
							line1 = line_text[line_split:].strip()
							a = line1.rfind('http://')
							line_name = line1[:a].strip()
							line_http =  line1[a:].strip()
					
							list_http.append (line_name)
							list_http.append (line_http)

																							
				with open(folder_patch + file_name, "w") as f:							#Сохраняем все в файл	
					for s in list_http:
						f.write(str(s) +"\n")
						#print(s)
				


		
		except requests.exceptions.RequestException as e:
			print('Сайт не отвечает. Проверьте соединение с итернетом.')
			sys.exit() 
	print('------------------------------------------')
	print('Работа скрипта завершена')	
	
	
open_list()			# 1 - читаем текстовой файл list.txt и здаем спискок с сылками и названиями плейлистов
folder_write()		# 2 - создаем папку для плейлистов
find_to_save()		# 3 - парсим и сохраняем в плейлист


