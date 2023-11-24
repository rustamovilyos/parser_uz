# import time
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# import os
#
#
# def filename_renamer(new_name):
#     download_path = 'books/downloaded_books'
#     renamed_path = 'books/renamed_books'
#     time.sleep(3)
#     files = os.listdir(download_path)
#     files = [f for f in files if os.path.isfile(os.path.join(download_path, f))]
#     # Find the latest file in the download directory
#     latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_path, x)))
#     time.sleep(3)
#     # Check whether a file with the desired name already exists in the renamed directory
#     if os.path.exists(f"{renamed_path}/{new_name}"):
#         print(f"File {new_name} already exists!")
#         return
#     # Check whether the file exists in the downloaded books directory
#     else:
#         if os.path.exists(f"{download_path}/{latest_file}"):
#             # Rename the file to the desired name
#             os.rename(f"{download_path}/{latest_file}", f"{renamed_path}/{new_name}")
#             print(f"File {latest_file} renamed successfully to {new_name}!\n"
#                   f"All files: {len(os.listdir(renamed_path))}")
#         else:
#             print(f"File {latest_file} does not exist in {download_path}")
#
#
# class Downloader:
#     def __init__(self, url, download_path):
#         self.url = url
#         self.download_path = download_path
#
#     def config(self):
#         options = Options()
#
#         options.add_argument("--headless")
#         options.set_preference("browser.helperApps.neverAsk.saveToDisk",
#                                "text/plain, application/vnd.ms-excel, text/csv,"
#                                "text/comma-separated-values, application/octet-stream")
#         options.set_preference("browser.download.dir", os.path.abspath(self.download_path))
#         options.set_preference("browser.download.folderList", 2)
#
#         return webdriver.Firefox(options=options)
#
#     def download(self):
#         driver = self.config()
#         try:
#             driver.get(self.url)
#             wait = WebDriverWait(driver, 10)
#             for i in range(1, 6):
#                 print(f"Book {i}")
#                 download_buttons = wait.until(EC.presence_of_all_elements_located(
#                     (By.CSS_SELECTOR,
#                      f"div.mantine-10wps28:nth-child({i}) > "
#                      f"div:nth-child(1) > div:nth-child(2) > "
#                      f"div:nth-child(1) > div:nth-child(1) > "
#                      f"div:nth-child(1) > div:nth-child(2) > "
#                      f"button:nth-child(1)")))
#                 books_title = wait.until(EC.presence_of_all_elements_located(
#                     (By.CSS_SELECTOR,
#                      f"div.mantine-10wps28:nth-child({i}) > "
#                      f"div:nth-child(1) > div:nth-child(1) > "
#                      f"a:nth-child(1)")))
#                 time.sleep(3)
#                 for buttons, title in zip(download_buttons, books_title):
#                     buttons.click()
#                     time.sleep(4)  # Wait for the download to complete (adjust the duration as needed)
#                     print(f"PDF file {title.text} downloaded successfully!")
#                     filename_renamer(f"{title.text}.pdf")
#                     driver.back()
#                     time.sleep(3)
#         except Exception as e:
#             print(e)
#
#         driver.quit()
#
#
# if __name__ == '__main__':
#     for page_num in range(4, 74):
#         print(f"Page {page_num}")
#         downloader = Downloader(f'https://library.ziyonet.uz/?type_id=30&page={page_num}&category_id=27&language_id=2',
#                                 '/home/ilyos/Work/projects/parser_uz/books/downloaded_books')
#         downloader.download()
#         driver = webdriver.Firefox()
#         driver.quit()
# for i in range(1, 6):
#     driver.get(f'https://library.ziyonet.uz/?type_id=30&page={i}&category_id=27&language_id=2')
#     print(f"Page {i} opened successfully!")
import os

import requests
import json

# https://library.ziyonet.uz/?type_id=30&page=1&language_id=5&category_id=27
url = "https://api.ziyonet.uz/api/uz/library?type_id=30&language_id=2&category_id=27"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

context = json.loads(response.content)
total_pages = context['pagination']['lastPage']
for page in range(1, total_pages + 1):
    print(f"Page {page}")
    new_link = f'https://api.ziyonet.uz/api/uz/library?type_id=30&language_id=2&category_id=27&page={page}'
    response = requests.get(new_link, allow_redirects=True)
    # print("response", response.content)
    data = response.json()

    for item in data['data']:
        title = item['title']
        file_url = item['file']

        # Скачивание файла
        file_response = requests.get(file_url)

        # Сохранение файла
        if os.path.exists(f"books/downloaded_books/{title}.pdf"):
            print(f"File {title}.pdf already exists!")
            break
        else:
            with open(f"books/downloaded_books/{title}.pdf", 'wb') as file:
                file.write(file_response.content)
                print(f"Файл {title}.pdf успешно скачан.")
