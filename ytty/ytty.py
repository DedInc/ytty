import os
from subprocess import Popen
from sys import platform
from time import sleep
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from requests import get
from vidspinner import unique
from pyperclip import copy as copy2clip
from keyboard import write, press
from pythread import createThread, stopThread

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
YT_DL_EXECUTABLE = os.path.join(CURRENT_DIR, 'ytdlp.exe')
YOUTUBE_SEARCH_URL = 'https://www.youtube.com/results?search_query={}&sp={}'
YOUTUBE_UPLOAD_URL = 'https://youtube.com/upload'
GOOGLE_SIGNIN_URL = 'https://accounts.google.com/signin'
DEFAULT_SEARCH_PERIODS = ('CAMSBAgCEAE=', 'CAMSBAgDEAE=', 'CAMSBAgEEAE=')

class Options:
    def add_option(self, option, value):
        setattr(self, option, value)

class YTOptions:
	def __init__(self):
		self.parse = Options()

		self.parse.add_option('search', 'Example search')
		self.parse.add_option('period', 2)
		self.parse.add_option('max', 20)

		self.download = Options()
		self.download.add_option('unique', False)

		self.upload = Options()
		self.upload.add_option('title', 'Example title')
		self.upload.add_option('description', None)
		self.upload.add_option('tags', [])
		self.upload.add_option('preview', None)
		self.upload.add_option('noKids', 1)
		self.upload.add_option('category', 12)
		self.upload.add_option('access', 'PUBLIC')

		self.upload.public = Options()
		self.upload.public.add_option('premiere', False)

def get_options(headless = False):
	options = ChromeOptions()
	if headless:
		options.add_argument('--headless')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--no-sandbox')
	options.add_argument('--no-first-run')
	options.add_argument('--no-service-autorun')
	options.add_argument('--lang=en-US')
	return options

def initer():
	return Chrome(options=get_options())

def shadow_session():
	return Chrome(options=get_options(True))

def google_session(login, password, ver=None):
	driver = initer()
	driver.get(GOOGLE_SIGNIN_URL)
	loginField = driver.find_element(By.ID, 'identifierId')
	actions = ActionChains(driver)
	actions.move_to_element(loginField).click().perform()
	write(login)
	sleep(0.5)
	press('enter')

	actions = ActionChains(driver)
	passwordField = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'password')))
	actions.move_to_element(passwordField).click().perform()
	write(password)
	sleep(0.5)
	press('enter')
	sleep(5)
	return driver

def get_ytdlp():	
	if not os.path.exists(YT_DL_EXECUTABLE):
		print('Install yt-dlp...')
		r = get('https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest').json()
		for asset in r['assets']:
			if 'x86' in asset['browser_download_url']:
				with open(ytdlp, 'wb') as f:
					f.write(get(asset['browser_download_url']).content)
				break
	return ytdlp

def get_video(link, options=YTOptions()):
	fname = '{}.mp4'.format(link.split('=')[1])
	p = Popen(f'{get_ytdlp()} "{link}" -f "mp4/bestvideo+bestaudio/best" -o "ytvideo.%(ext)s"')
	p.communicate()
	for file in listdir():
		if 'ytvideo' in file:
			if options.download.unique:
				unique(file, fname)
				remove(file)
			else:
				rename(file, fname)
	return fname

def get_thumbnail(vid):
	mrd = f'https://img.youtube.com/vi/{vid}/maxresdefault.jpg'
	d = f'https://img.youtube.com/vi/{vid}/0.jpg'
	fname = f'{vid}.jpg'
	with open(fname, 'wb') as f:
		f.write(get(mrd).content)
	if getsize(fname) == 1097:
		with open(fname, 'wb') as f:
			f.write(get(d).content)
	return fname

def notify_closer():
	try:
		closeNotify = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#close-button')))
		click(driver, closeNotify)
	except:
		pass

def upload_video(driver, options):
	driver.get(YOUTUBE_UPLOAD_URL)

	try:
		dismiss = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#dismiss-button')))
		dismiss.click()
	except:
		pass

	t = createThread('NotifyCloser', notify_closer, 0.1)
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
	descriptionElem = textboxes[len(textboxes) - 3]

	driver.execute_script('arguments[0].innerText = \'\'', titleElem)
	set_value(driver, titleElem, options.upload.title)
	set_value(driver, descriptionElem, options.upload.description)

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

	set_value(driver, tagsElem, tags)

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

	stopThread(t)

def parse_videos(driver, options):
	parseList = []
	i = 0	
	searchUrl = YOUTUBE_SEARCH_URL.format(options.parse.search.replace(' ', '+'), DEFAULT_SEARCH_PERIODS[options.parse.period])
	driver.get(searchUrl)
	videos = driver.find_elements(By.CSS_SELECTOR, 'a#video-title')
	for video in videos:
		if i >= options.parse.max:
			break
		parseList.append({'title': video.get_attribute('title'), 'link': video.get_attribute('href'), 'id': video.get_attribute('href').split('=')[1]})
		i += 1
	return parseList

def set_value(driver, element, value):
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