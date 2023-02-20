import requests
from bs4 import BeautifulSoup
import re
import csv
import sys


# 執行就能爬取 https://iqc.tw/taiwan-food-safety-incident 的所有新聞
# 儲存方式為 csv , header = [ "news_link","news_text" ]
# 新聞預先做處理，去除特殊字元和換行

HEADERS = {
	'authority': 'iqc.tw',
	'method': 'GET',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

# get news from link


def get_news_from_link( link:str ):

	news = ""
	url = requests.get(link,headers=HEADERS)
	soup = BeautifulSoup(url.text,"html.parser")

	news = soup.select("div.entry-content")[0].getText()

	news = re.sub("連結.*\n","",news)
	news = re.sub("小編評：.*\n","" , news)
	news = re.sub("[\u3000|\u2002|\xa0|\u200b|\n| ]" ,'' ,news)


	return str(news)



# get all links from event group

def get_event_news_list(event_link: str):

	temp = []

	url = requests.get(event_link, headers=HEADERS)
	soup = BeautifulSoup(url.text, "html.parser")

	# get all news link & remove main page
	temp += [s["href"] for s in soup.select("h2.entry-title>a")
											if s["href"].find("taiwan-food-safety-incident") == -1]

	# check if more than one page
	next_page = soup.select("a.next.page-numbers")

	if len(next_page):
		# go to next page
		temp += get_event_news_list(next_page[0]["href"])

	return temp


def main():

	print('start')

 	# csvfile name
	target_csv = "iqc_food_news.csv"

 	# max data count
	max_data_count = 1000

 	# home page
	url = requests.get(
		"https://iqc.tw/taiwan-food-safety-incident", headers=HEADERS)
	soup = BeautifulSoup(url.text, "html.parser")

	# event page
	event_links = [x["href"] for x in soup.select("p>a")[1:]]

	with open( target_csv ,'w' , newline='', encoding='utf-8' ) as f:

		writer = csv.writer(f , delimiter=',' )
		writer.writerow(["news_link","news_text"])

		for link in event_links:

			link_temp = get_event_news_list(link)

			if len(link_temp)==0:
				link_temp = [link]

			print( f"this title has {len(link_temp)} news to parse")

			for e_link in link_temp:

				try:
					n = get_news_from_link(e_link)
					if len(n):
						writer.writerow([ str(e_link) , n])
						max_data_count -=1
					else:
						continue
				except:
					print(f"link error {str(e_link)}")
					continue

				if not max_data_count:
					break

			if not max_data_count:
				break
	print("done")

if __name__ == '__main__':
	main()