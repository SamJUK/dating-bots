import time
import random

def randomSeconds(min, max):
	return random.randrange(min*100, max*100) / 100

def pageSleep(min=.8, max=4.5):
	randomSleep(min, max)

def interactionSleep(min=1.6, max=6):
	randomSleep(min, max)

def randomSleep(min=.5, max=2):
	sleep(randomSeconds(min, max))

def sleep(length):
	time.sleep(length)