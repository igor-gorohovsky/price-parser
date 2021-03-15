from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ChromeBrowser():

	def __init__(self):
		options = Options()
		options.add_argument("--headless")

		try:			
			self.driver = webdriver.Chrome(options=options)
		except Exception as e:
			self.driver.quit()
			print(e)


	def tear_down(self):
		self.driver.quit()