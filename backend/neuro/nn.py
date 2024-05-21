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
    text = pytesseract.image_to_string(img1, lang=language)
    return text


# Function to perform OCR on a page
# def ocr_page(page, language):
#     pix = page.get_pixmap()
#     img = Image.open(io.BytesIO(pix.tobytes()))
#
#     ocr_data = pytesseract.image_to_data(img, lang=language,
#                                          output_type=pytesseract.Output.DICT)
#     # pprint.pprint(ocr_data)
#     char_data = pytesseract.image_to_boxes(img,config='tosp_near_lh_edge=1', lang=language, output_type=pytesseract.Output.DICT)
#     return ocr_data, char_data, img.size
#
#
# # Read and OCR the PDF
# def rect_avg_color(page, x, y, w, h):
#     pix = page.get_pixmap()
#     img = Image.open(io.BytesIO(pix.tobytes()))
#     r, g, b = 0, 0, 0
#     for i in range(x, x + w):
#         for j in range(y, y + h):
#             current_r, current_g, current_b = img.getpixel((i, j))
#             r += current_r
#             g += current_g
#             b += current_b
#     r /= w * h * 255
#     g /= w * h * 255
#     b /= w * h * 255
#     avg_color = (r, g, b)
#     return avg_color
# , config='--psm 3 --oem 3'

# def ocr_pdf(pdf_path, language):
#     draw_box = True
#     box_fill = True
#     doc = fitz.open(pdf_path)
#     total_pages = len(doc)
#     print(f"Total pages in the document: {total_pages}")
#
#     for page_num in range(0, total_pages):
#         print(f"Processing page {page_num + 1}/{total_pages}...")
#         page = doc[page_num]
#         ocr_data, char_data, img_size = ocr_page(page, language)
#         page.clean_contents()
#         print(char_data.keys())
#         for i, char in enumerate(char_data['char']):
#             l, b, r, t = char_data['left'][i], char_data['bottom'][i], char_data['right'][i], char_data['top'][i]
#             print(char, l, b, r, t)
#             shape = page.new_shape()
#             # if t-b>(r-l)*2:
#             #     continue
#             shape.draw_rect((l,img_size[1]-t,r,img_size[1]-b))
#             shape.finish(color=(1, 0, 0), width=0.1)
#             shape.commit(overlay=True)
#             # page.insert_text((x, y + h), word, fontsize=8, color=white)
#         continue
#         for i, word in enumerate(ocr_data['text']):
#             if word.strip():  # Exclude empty strings
#                 x, y, w, h, = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
#                 white = (0, 0, 0)
#                 if draw_box:
#                     shape = page.new_shape()
#                     shape.draw_rect((x, y, x + w, y + h))
#                     if box_fill:
#                         avg_color = rect_avg_color(page, x, y, w, h)
#                         shape.finish(color=avg_color, width=0.1, fill=avg_color)
#                     else:
#                         shape.finish(color=(1, 0, 0), width=1)
#                     shape.commit(overlay=True)
#                 page.insert_text((x, y + h), word, fontsize=8, color=white)
#                 # print(word)
#
#     print("OCR process completed.")
#     return doc


# def process_pdf(pdf_path, language):
#     start_page = 1
#     end_page = None
#
#     output_path = pdf_path.rsplit('.', 1)[0] + '-converted.pdf'  # Add '-converted' suffix to the filename
#
#     print(f"Starting OCR for {pdf_path}...")
#     doc = ocr_pdf(pdf_path, language)
#     doc.save(output_path)  # Save the searchable PDF
#     print(f"Converted PDF saved as {output_path}")


def prepare_folders(image_folder: str, text_folder: str) -> None:
    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(text_folder, exist_ok=True)


def parse(url: str, language: str, result_name: str) -> tuple[str, str, str]:
    # url = "http://www.proinfosystem.com/articles/hidden.html"
    # language = "rus"

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
