import pprint
from typing import Tuple, Any

from PIL import Image
import pytesseract
import numpy as np
import time
import os

# import sys
# import fitz  # PyMuPDF
# import io

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from chrome_extension_python import Extension


def saveUrlToImage(url, resultImageName):
    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')

    # proxy_server_url = "localhost:8118"
    # options.add_argument(f'--proxy-server={proxy_server_url}')

    print('initial setup done')
    adblockers = ["https://chromewebstore.google.com/detail/ghostery-блокировщик-трек/mlomiejdfkolichcflejclcbmpeaniij",
                  "https://chromewebstore.google.com/detail/adguard-антибаннер/bgnkhhnnamicmpeenaelnjfhikgbkllg",
                  # "https://chromewebstore.google.com/detail/adblocker-stands/lgblnfidahcdcjddiepkckcfdhpknnjh",
                  # "https://chromewebstore.google.com/detail/adblock-%E2%80%94-best-ad-blocker/gighmmpiobklfepjocnamgkkbiglidom",
                  "https://chromewebstore.google.com/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm",
                  "https://chromewebstore.google.com/detail/stop-reclame/ohmkcnojelglgphmkgmofjlmpoelccjh"]
    options.add_argument('--load-extension=' + ','.join(
        [Extension(adblocker).load(with_command_line_option=False) for adblocker in adblockers]))

    print('extensions setup done')
    driver = Chrome(options=options)
    driver.maximize_window()

    print('opening done')
    driver.get(url)

    time.sleep(20)
    print('get url done')

    num_of_tabs = len(driver.window_handles)
    for x in range(1, num_of_tabs):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 'W')
        print(x)
        time.sleep(1)
    print('close extra tabs done')

    time.sleep(10)
    width = driver.execute_script(
        "return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
    height = driver.execute_script(
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    print('resized page')

    driver.set_window_size(width, height)

    full_page = driver.find_element(By.TAG_NAME, "body")
    full_page.screenshot(resultImageName)

    driver.quit()
    print('SCREENSHOT DONE', os.listdir())


def imageToText(image_path, language):
    img1 = np.array(Image.open(image_path))
    # https://ru.wikipedia.org/wiki/Tesseract
    text = pytesseract.image_to_string(img1, lang=language)
    return text


def prepare_folders(image_folder: str, text_folder: str) -> None:
    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(text_folder, exist_ok=True)


def parse(url: str, language: str, result_name: str) -> tuple[str, str, str]:
    image_folder = './images'
    text_folder = './texts'
    prepare_folders(image_folder, text_folder)

    image_path = f"{image_folder}/{result_name}.png"
    saveUrlToImage(url, image_path)
    text = imageToText(image_path, language)

    text_path = f"{text_folder}/{result_name}.txt"
    with open(text_path, "w", encoding="utf-8") as file:
        file.write(text)

    return text, image_path, text_path


if __name__ == "__main__":
    print(parse('https://www.rbc.ru/', 'rus+eng', 'rbc'))
