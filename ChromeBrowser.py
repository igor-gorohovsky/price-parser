from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ChromeBrowser():

	def __init__(self):
		options = Options()
		options.add_argument("--headless")		
		self.driver = webdriver.Chrome(options=options)



	def close(self):
		self.driver.quit()


	def get(self, url):
		return self.driver.get(url)