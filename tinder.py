import lib.common.time as time
import lib.common.browser as browser

from lib.tinder.client import Client
from credentials.tinder import facebook_credentials

driver = browser.createBrowser()

session = Client(driver)
session.login(facebook_credentials)
time.pageSleep()

while True:
	time.interactionSleep()
	print("-" * 15)
	session.processUser()