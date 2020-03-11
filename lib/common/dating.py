from abc import ABCMeta, abstractmethod
from selenium.webdriver.support import ui

class IDating:
	__metaclass__ = ABCMeta

	@classmethod
	def version(self): return '1.0'

	@abstractmethod
	def login(self, credentials): raise NotImplementedError

	@abstractmethod
	def processUser(self): raise NotImplementedError

	@abstractmethod
	def like(self): raise NotImplementedError

	@abstractmethod
	def dislike(self): raise NotImplementedError

	def loginWithFacebook(self, credentials):
		wait = ui.WebDriverWait(self.driver, 10)
		previous_window = self.driver.window_handles[0]
		facebook_window = self.driver.window_handles[-1]
		self.driver.switch_to.window(facebook_window)

		wait.until(lambda driver: self.driver.find_element_by_xpath(self.node_selectors["facebook_username"]))
		self.driver.find_element_by_xpath(self.node_selectors["facebook_username"]).send_keys(credentials["username"])
		self.driver.find_element_by_xpath(self.node_selectors["facebook_password"]).send_keys(credentials["password"])
		self.driver.find_element_by_xpath(self.node_selectors["facebook_login_trigger"]).click()

		self.driver.switch_to.window(previous_window)
		return self