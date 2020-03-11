import math
import random

import lib.common.time as time
import lib.common.browser as browser
from lib.common.dating import IDating

from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

class Client(IDating):

	node_selectors = {
		"bumble_fb_login_trigger": '//*[contains(@class, "color-provider-facebook") and .//span[contains(., "Use Facebook")]]',
		"facebook_username": '//*[@id="email"]',
		"facebook_password": '//*[@id="pass"]',
		"facebook_login_trigger": '//input[@name="login"]',
		"bumble_stories_container": '//div[contains(@class, "encounters-album__stories-container")]',
		"bumble_stories": '//div[contains(@class, "encounters-album__stories-container")]/*',
		"bumble_user_name_age": '//*[contains(@class, "encounters-story-profile__name")]',
		"bumble_no_users_dialog": '//*[contains(@class, "cta-box__title") and .//span[contains(., "all caught up")]]'
	}

	def __init__(self, driver):
		self.driver = driver

	def login(self, credentials):
		self.driver.get('https://bumble.com/get-started')
		wait = ui.WebDriverWait(self.driver, 10)
		wait.until(lambda driver: self.driver.find_element_by_xpath(self.node_selectors["bumble_fb_login_trigger"]))
		self.loginWithFacebook(credentials)
		return self

	def getName(self):
		return self.driver.find_element_by_xpath(self.node_selectors["bumble_user_name_age"]).text.split(',')[0]

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
			self.driver.find_element_by_xpath(self.node_selectors["bumble_no_users_dialog"])
			return True
		except NoSuchElementException:
			return False

	def processUser(self):
		wait = ui.WebDriverWait(self.driver, 10)
		wait.until(lambda driver: self.driver.find_element_by_xpath(
			"{} | {}".format(self.node_selectors["bumble_stories_container"], self.node_selectors["bumble_no_users_dialog"])
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
		stories = self.driver.find_elements_by_xpath(self.node_selectors["bumble_stories"])
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