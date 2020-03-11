import math
import random

import lib.common.time as time
from lib.common.dating import IDating

from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

class Client(IDating):
	node_selectors = {
		"facebook_username": '//*[@id="email"]',
		"facebook_password": '//*[@id="pass"]',
		"facebook_login_trigger": '//input[@name="login"]',
		"tinder_login_model_trigger": '//button[.//span[contains(.,"Log in")]]',
		"tinder_login_model": '//div[@id="modal-manager" and .//*[contains(.,"Get started")]]',
		"tinder_login_more_options": '//button[contains(.,"More options")]',
		"tinder_login_facebook": '//button[.//*[contains(.,"Login with Facebook")]]',
		"tinder_popup_model_accept": '//*[@id="modal-manager"] //button[.//span[contains(.,"Allow")]]',
		"tinder_user_card": '(//div[contains(@class, "recCard") and @aria-hidden="false"]',
		"tinder_user_gallery": '//div[contains(@class, "recCard") and @aria-hidden="false"] //div[contains(@class, "react-swipeable-view-container")] //div[@data-swipeable="true"]',
		"tinder_user_name": '(//div[contains(@class, "recCard") and @aria-hidden="false"] //div[contains(@class, "recCard__info")] //span)[1]'
	}

	def __init__(self, driver):
		self.driver = driver

	def login(self, credentials):
		self.driver.get('https://tinder.com/')
		wait = ui.WebDriverWait(self.driver, 10)

		# Wait for the login model
		try:		
			wait.until(lambda driver: self.driver.find_element_by_xpath(self.node_selectors["tinder_login_model"]))
		except TimeoutException:
			self.driver.find_element_by_xpath(self.node_selectors["tinder_login_model_trigger"]).click()
			wait.until(lambda driver: self.driver.find_element_by_xpath(self.node_selectors["tinder_login_model"]))

		try:
			self.driver.find_element_by_xpath(self.node_selectors["tinder_login_more_options"]).click()
		except NoSuchElementException:
			pass

		self.driver.find_element_by_xpath(self.node_selectors["tinder_login_facebook"]).click()
		self.loginWithFacebook(credentials)

		return self

	def getName(self):
		return self.driver.find_element_by_xpath(self.node_selectors["tinder_user_name"]).text

	def like(self):
		print('Liked')
		actions = ActionChains(self.driver)
		actions.send_keys(Keys.ARROW_RIGHT)
		actions.perform()
		return self

	def dislike(self):
		actions = ActionChains(self.driver)
		actions.send_keys(Keys.ARROW_RIGHT)
		actions.perform()
		return self

	def acceptPopupModel(self):
		self.driver.find_element_by_xpath(self.node_selectors["tinder_popup_model_accept"]).click()
		return self

	def acceptAllPopupModels(self):
		try:
			self.acceptPopupModel()
			# Wait for new popups
			time.interactionSleep(1.2,1.6)
			self.acceptAllPopupModels();
		except NoSuchElementException:
			pass

		return self

	def processUser(self):
		self.acceptAllPopupModels()

		try:
			wait = ui.WebDriverWait(self.driver, 10)
			wait.until(lambda driver: self.driver.find_element_by_xpath(self.node_selectors["tinder_user_card"]))
		except NoSuchElementException:
			print("No user data")
			time.randomSleep(300, 1200)
			return self
		except TimeoutException:
			print("No user data")
			time.randomSleep(300, 1200)
			return self

		print("Processing user: {}".format(self.getName()))
		self.interactWithContent()
		time.interactionSleep(.5, 1)

		if random.randrange(0, 100) < 73:
			self.like()
		else:
			self.dislike()

		return self

	def interactWithContent(self):
		self.interactWithGallery()
		# @TODO: Open profile and scroll a bit?
		return self

	def interactWithGallery(self):
		images = self.driver.find_elements_by_xpath(self.node_selectors["tinder_user_gallery"])
		imageCount = len(images)
		imageCycleCount = random.randrange(0, math.ceil((imageCount-1)*1.2))

		for _ in range(imageCycleCount):
			actions.send_keys(Keys.SPACE)
			actions.perform()
			time.interactionSleep(.7, 1.8)

		return self