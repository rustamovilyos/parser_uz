import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import shutil


def filename_renamer(new_name):
    download_path = 'books/downloaded_books'
    files = os.listdir(download_path)
    for file in files:
        if os.path.isfile(os.path.join(download_path, file)):
            if files:
                latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_path, x)))
                print(f"Latest file: {latest_file}")
                os.rename(f"books/downloaded_books/{latest_file}", f"books/renamed_books/{new_name}")
                print(f"File {latest_file} renamed successfully!")
            else:
                print("Папка скачивания пуста или отсутствуют файлы.")


class Downloader:
    def __init__(self, url, download_path):
        self.url = url
        self.download_path = download_path

    def config(self):
        options = Options()

        options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "text/plain, application/vnd.ms-excel, text/csv,"
                               "text/comma-separated-values, application/octet-stream")
        options.set_preference("browser.download.dir", os.path.abspath(self.download_path))
        options.set_preference("browser.download.folderList", 2)

        return webdriver.Firefox(options=options)

    def download(self):
        driver = self.config()
        try:
            driver.get(self.url)
            wait = WebDriverWait(driver, 10)
            for i in range(1, 6):
                download_buttons = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR,
                     f"div.mantine-10wps28:nth-child({i}) > "
                     f"div:nth-child(1) > div:nth-child(2) > "
                     f"div:nth-child(1) > div:nth-child(1) > "
                     f"div:nth-child(1) > div:nth-child(2) > "
                     f"button:nth-child(1)")))
                books_title = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR,
                     f"div.mantine-10wps28:nth-child({i}) > "
                     f"div:nth-child(1) > div:nth-child(1) > "
                     f"a:nth-child(1)")))
                time.sleep(2)
                for buttons, title in zip(download_buttons, books_title):
                    buttons.click()
                    time.sleep(10)  # Wait for the download to complete (adjust the duration as needed)
                    print(f"PDF file {title.text} downloaded successfully!")
                    filename_renamer(f"{title.text}.pdf")
                    driver.back()
                    time.sleep(3)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    for page_num in range(1, 74):
        downloader = Downloader(f'https://library.ziyonet.uz/?type_id=30&page={page_num}&category_id=27&language_id=2',
                                '/home/ilyos/Work/projects/parser_uz/books/downloaded_books')
        downloader.download()
        driver = webdriver.Firefox()
    # for i in range(1, 6):
    #     driver.get(f'https://library.ziyonet.uz/?type_id=30&page={i}&category_id=27&language_id=2')
    #     print(f"Page {i} opened successfully!")
