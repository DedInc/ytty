from os import environ as env, access, sep, listdir, X_OK, rename, remove
from os.path import exists, normpath, getsize, abspath, dirname, join as pjoin
from subprocess import Popen
from sys import platform
from time import sleep
from threading import Thread
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from requests import get
from vidspinner import unique
from pyperclip import copy as copy2clip

CDIR = abspath(dirname(__file__))

class Options:
	def __init__(self):
		pass

	def addOption(self, option, value):
		exec(f'self.{option} = value')

class YTOptions:
	def __init__(self):
		self.parse = Options()
		self.parse.addOption('search', 'Example search')
		self.parse.addOption('period', 2)
		self.parse.addOption('max', 20)
		self.download = Options()
		self.download.addOption('unique', False)
		self.upload = Options()
		self.upload.addOption('title', 'Example title')
		self.upload.addOption('description', None)
		self.upload.addOption('tags', [])
		self.upload.addOption('preview', None)
		self.upload.addOption('noKids', 1)
		self.upload.addOption('category', 12)
		self.upload.addOption('access', 'PUBLIC')
		self.upload.public = Options()
		self.upload.public.addOption('premiere', False)

def getChrome():
	global version
	candidates = set()
	for item in map(
		env.get, ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")
	):
		for subitem in (
			"Google/Chrome/Application",
			"Google/Chrome Beta/Application",
			"Google/Chrome Canary/Application",
		):
			try:
				candidates.add(sep.join((item, subitem, "chrome.exe")))
			except:
				pass
	for candidate in candidates:
		if exists(candidate) and access(candidate, X_OK):
			path = normpath(candidate)
			version = int(listdir(path.split('Application')[0] + 'Application')[0].split('.')[0])
			return path

def initer():
	options = ChromeOptions()
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--no-sandbox')
	options.add_argument('--no-first-run')
	options.add_argument('--no-service-autorun')
	options.add_argument('--lang=en-US')
	if 'win' in platform:
		options.binary_location = getChrome()
		ver = version
	return Chrome(options=options, version_main=ver)

def shadowSession():
	options = ChromeOptions()
	options.add_argument('--headless')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--no-sandbox')
	options.add_argument('--no-first-run')
	options.add_argument('--no-service-autorun')
	options.add_argument('--lang=en-US')
	if 'win' in platform:
		options.binary_location = getChrome()
		ver = version
	return Chrome(options=options, version_main=ver)

def googleSession(login, password, ver=None):
	driver = initer()
	driver.get('https://accounts.google.com/signin')
	loginField = driver.find_element(By.ID, 'identifierId')
	nextButton = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
	actions = ActionChains(driver)
	actions.move_to_element(loginField).click().send_keys(login).perform()
	actions.move_to_element(nextButton).click().perform()
	sleep(3)
	passwordField = driver.find_element(By.ID, 'password')
	actions.move_to_element(passwordField).click().send_keys(password).perform()
	nextButton = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
	actions.move_to_element(nextButton).click().perform()
	sleep(3)
	return driver

def getYTDlp():
	ytdlp = pjoin(CDIR, 'ytdlp.exe')
	if not exists(ytdlp):
		print('Install yt-dlp...')
		r = get('https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest').json()
		for asset in r['assets']:
			if 'x86' in asset['browser_download_url']:
				with open(ytdlp, 'wb') as f:
					f.write(get(asset['browser_download_url']).content)
				break
	return ytdlp

def getVideo(link, options=YTOptions()):
	fname = '{}.mp4'.format(link.split('=')[1])
	p = Popen(f'{getYTDlp()} "{link}" -f "mp4/bestvideo+bestaudio/best" -o "ytvideo.%(ext)s"')
	p.communicate()
	for file in listdir():
		if 'ytvideo' in file:
			if options.download.unique:
				unique(file, fname)
				remove(file)
			else:
				rename(file, fname)
	return fname

def getThumbnail(vid):
	mrd = f'https://img.youtube.com/vi/{vid}/maxresdefault.jpg'
	d = f'https://img.youtube.com/vi/{vid}/0.jpg'
	fname = f'{vid}.jpg'
	with open(fname, 'wb') as f:
		f.write(get(mrd).content)
	if getsize(fname) == 1097:
		with open(fname, 'wb') as f:
			f.write(get(d).content)
	return fname

def notifyCloser():
	while True:
		try:
			closeNotify = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#close-button')))
			click(driver, closeNotify)
		except:
			pass

def uploadVideo(driver, options):
	driver.get('https://youtube.com/upload')

	try:
		dismiss = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#dismiss-button')))
		dismiss.click()
	except:
		pass

	t = Thread(target=notifyCloser)
	t.start()

	inputs = driver.find_elements(By.TAG_NAME, 'input')
	for input in inputs:
		if input.get_attribute('type') == 'file':
			picker = input
			break
	picker.send_keys(abspath(options.upload.video))

	WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#textbox')))

	textboxes = driver.find_elements(By.CSS_SELECTOR, 'div#textbox')
	titleElem = textboxes[len(textboxes) - 2]
	driver.execute_script('arguments[0].innerText = \'\'', titleElem)
	descriptionElem = textboxes[len(textboxes) - 3]

	setValue(driver, titleElem, options.upload.title)
	setValue(driver, descriptionElem, options.upload.description)

	inputs = driver.find_elements(By.TAG_NAME, 'input')
	for input in inputs:
		if input.get_attribute('type') == 'file':
			thumbnail = input
			break

	thumbnail.send_keys(abspath(options.upload.preview))

	kids = driver.find_elements(By.CSS_SELECTOR, 'ytcp-ve.ytkc-made-for-kids-select')
	click(driver, kids[options.upload.noKids])

	sm = driver.find_element(By.CSS_SELECTOR, 'ytcp-button#toggle-button')
	click(driver, sm)

	tags = ''
	for tag in options.upload.tags:
		tags += tag + ','

	tagsElem = driver.find_element(By.CSS_SELECTOR, 'input#text-input[aria-label]')

	setValue(driver, tagsElem, tags)

	ytstrings = driver.find_elements(By.CSS_SELECTOR, 'yt-formatted-string')
	for i in range(len(ytstrings) - 1, len(ytstrings) - 16):
		if len(ytstrings) - 1 - i == options.upload.category:
			click(driver, ytstrings[i])
			break
		i -= 1

	nextButton = driver.find_element(By.ID, 'next-button')
	click(driver, nextButton)
	WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ytcp-uploads-video-elements')))
	click(driver, nextButton)
	WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.feedback-text')))
	click(driver, nextButton)
	WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tp-yt-paper-radio-button[name=FIRST_CONTAINER]')))

	access = driver.find_element(By.CSS_SELECTOR, f'tp-yt-paper-radio-button[name={options.upload.access}]')
	click(driver, access)

	if options.upload.access == 'PUBLIC' and options.upload.public.premiere:
		checkBoxPremiere = driver.find_element(By.CSS_SELECTOR, '#enable-premiere-checkbox')
		click(driver, checkBoxPremiere)

	publish = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#done-button:not([disabled])')))
	click(driver, publish)
	while len(driver.find_elements(By.CSS_SELECTOR, 'ytcp-video-upload-progress[uploading]')) != 0:
		pass
	t.join()

def parseVideos(driver, options):
	parseList = []
	i = 0
	sps = ('CAMSBAgCEAE=', 'CAMSBAgDEAE=', 'CAMSBAgEEAE=')
	searchUrl = 'https://www.youtube.com/results?search_query={}&sp={}'.format(options.parse.search.replace(' ', '+'), sps[options.parse.period])
	driver.get(searchUrl)
	videos = driver.find_elements(By.CSS_SELECTOR, 'a#video-title')
	for video in videos:
		if i >= options.parse.max:
			break
		parseList.append({'title': video.get_attribute('title'), 'link': video.get_attribute('href'), 'id': video.get_attribute('href').split('=')[1]})
		i += 1
	return parseList

def setValue(driver, element, value):
	i = 0
	while i != 5:
		try:
			copy2clip(value)
			actions = ActionChains(driver)
			actions.move_to_element(element).click().key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
			break
		except:
			i += 1
			sleep(3)

def click(driver, element):
	driver.execute_script("arguments[0].click()", element)