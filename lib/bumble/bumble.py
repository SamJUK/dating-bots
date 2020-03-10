import math
import random
import lib.common.time as time

import lib.common.browser as browser
from lib.bumble.config import node_selectors

from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class Bumble:
	def __init__(self, driver):
		self.driver = driver

	def login(self, credentials):
		self.driver.get('https://bumble.com/get-started')
		wait = ui.WebDriverWait(self.driver, 10)
		wait.until(lambda driver: self.driver.find_element_by_xpath(node_selectors["bumble_fb_login_trigger"]))

		bumble_window = self.driver.window_handles[0]
		self.driver.find_element_by_xpath(node_selectors["bumble_fb_login_trigger"]).click()
		facebook_window = self.driver.window_handles[-1]
		self.driver.switch_to.window(facebook_window)

		# Wait for facebook inputs, enter and submit
		wait.until(lambda driver: self.driver.find_element_by_xpath(node_selectors["facebook_username"]))
		self.driver.find_element_by_xpath(node_selectors["facebook_username"]).send_keys(credentials["username"])
		self.driver.find_element_by_xpath(node_selectors["facebook_password"]).send_keys(credentials["password"])
		self.driver.find_element_by_xpath(node_selectors["facebook_login_trigger"]).click()

		self.driver.switch_to.window(bumble_window)
		return self

	def getName(self):
		return self.driver.find_element_by_xpath(node_selectors["bumble_user_name_age"]).text

	def like(self):
		print('Liked')
		actions = ActionChains(self.driver)
		actions.send_keys(Keys.ARROW_RIGHT)
		actions.perform()
		return self

	def dislike(self):
		print('Disliked')
		actions = ActionChains(self.driver)
		actions.send_keys(Keys.ARROW_LEFT)
		actions.perform()
		return self

	def noUserDialog(self):
		try:
			self.driver.find_element_by_xpath(node_selectors["bumble_no_users_dialog"])
			return True
		except NoSuchElementException:
			return False

	def processUser(self):
		wait = ui.WebDriverWait(self.driver, 10)
		wait.until(lambda driver: self.driver.find_element_by_xpath(
			"{} | {}".format(node_selectors["bumble_stories_container"], node_selectors["bumble_no_users_dialog"])
		))

		if self.noUserDialog():
			print("No Users left to process")
			time.randomSleep(300, 1200)
			return self

		print("Processing user: {}".format(self.getName()))
		self.scrollContent()

		time.interactionSleep(.3, .8)

		if random.randrange(0, 100) < 73:
			self.like()
		else:
			self.dislike()

		return self

	def scrollContent(self):
		actions = ActionChains(self.driver)
		stories = self.driver.find_elements_by_xpath(node_selectors["bumble_stories"])
		storyCount = len(stories)
		totalNavigationActions = random.randrange(0, math.ceil((storyCount-1)*1.2))
		currentStory = 0
	
		print("Scrolling {} times on {} stories".format(totalNavigationActions, storyCount))

		for _ in range(totalNavigationActions):
			if currentStory == 0:
				actions.send_keys(Keys.ARROW_DOWN)
			elif currentStory == (storyCount - 1):
				actions.send_keys(Keys.ARROW_UP)
			else:
				actions.send_keys(random.choice([Keys.ARROW_UP, Keys.ARROW_DOWN]))

			actions.perform()
			currentStory += 1
			time.interactionSleep()

		return self