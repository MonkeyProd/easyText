import pprint

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


def saveUrlToImage(url, resultImageName):
    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')

    driver = Chrome(options=options)
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


def parse(url, language, image_name):
    filename = image_name
    # url = "http://www.proinfosystem.com/articles/hidden.html"
    # language = "rus"

    path = './images'

    saveUrlToImage(url, f"{path}/{filename}")
    text = imageToText(f"{path}/{filename}.png", language)

    text_filename = f"./texts/{filename}.txt"
    with open(text_filename, "w", encoding="utf-8") as file:
        file.write(text)

    return text


if __name__ == "__main__":
    # print(imageToText('test.png', 'eng'))
    process_pdf('test.pdf', 'eng')
