from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def createBrowser():
	opts = Options()
	opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36")
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
	driver.set_window_size(1024, 768)
	return driver