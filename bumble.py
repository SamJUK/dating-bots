import lib.common.time as time
import lib.common.browser as browser

from lib.bumble.bumble import Bumble
from credentials.bumble import facebook_credentials

driver = browser.createBrowser()

session = Bumble(driver)
session.login(facebook_credentials)
time.pageSleep()

while True:
	time.interactionSleep()
	print("-" * 15)
	session.processUser()