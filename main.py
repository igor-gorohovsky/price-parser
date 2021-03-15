from selenium import webdriver
from selenium.webdriver.chrome.options import Options


driver = ""


# Open browser in headless mode
def set_up():
	try:
		options = Options()
		options.add_argument("--headless")
		global driver
		driver = webdriver.Chrome(options=options)
	except Exception as e:
		driver.quit()
		print(e)


# Close the browser after working
def tear_down():
	driver.quit()	


def main():
	set_up()
	page = driver.get("http://www.google.com")
	assert "Google" in driver.title
	tear_down()


if __name__ == '__main__':
	main()
