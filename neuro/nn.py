from PIL import Image
import pytesseract
import numpy as np
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

filename = "image"
url = "http://www.proinfosystem.com/articles/hidden.html"
language = "rus"

path = os.path.dirname(os.path.abspath(__file__))


def saveUrlToImage(url, resultImageName):
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get(url)

    time.sleep(1)

    width = driver.execute_script(
        "return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
    height = driver.execute_script(
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

    driver.set_window_size(width, height)

    full_page = driver.find_element(By.TAG_NAME, "body")
    full_page.screenshot(f"{resultImageName}.png")

    driver.quit()


def imageToText(image_path, language):
    img1 = np.array(Image.open(image_path))
    text = pytesseract.image_to_string(img1, lang=language)
    return text


path = os.path.dirname(os.path.abspath(__file__))

saveUrlToImage(url, filename)
text = imageToText(f"{path}\{filename}.png", language)

text_filename = "text.txt"
with open(text_filename, "w", encoding="utf-8") as file:
    file.write(text)

print(text)
