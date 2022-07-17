from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from get_urls import get_urls
from PIL import Image
import img2pdf
import pickle
import random
import time
import json
import os


def urls(website):
    pages = []
    get_urls(website)
    f = open('data.json')
    data = json.load(f)
    f.close()
    for key, value in data.items():
        if not value[1]:
            pages.append(key)
    return reversed(pages)


def setup(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    return driver


def screenshot(driver, url, name):
    driver.get(url)
    time.sleep(random.random())
    s = driver.get_window_size()
    # obtain browser height and width
    width = 1920
    height = driver.execute_script('return document.body.parentNode.scrollHeight')
    # set to new window size
    driver.set_window_size(width, height)
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    driver.set_window_size(S('Width'), S('Height'))
    driver.find_element(By.TAG_NAME, 'body').screenshot(f'{name}.png')
    # f'output/{count}.png'


def image_to_pdf(name):
    image = Image.open(f'{name}.png')
    # converting into chunks using img2pdf
    pdf_bytes = img2pdf.convert(image.filename)
    # opening or creating pdf file
    file = open(f'{name}.pdf', "wb")
    # writing pdf files with chunks
    file.write(pdf_bytes)
    # closing image file
    image.close()
    os.remove(f'{name}.png')
    # closing pdf file
    file.close()
