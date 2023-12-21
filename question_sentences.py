from datetime import datetime
import glob
import os
import re

from PyPDF2 import PdfReader
from fitrat import Transliterator, WritingType
import csv

from pdf2image import convert_from_path
import fitz
from image_parser import image_to_string

extended = []


def logger(printing):
    log_file = open("log.txt", "a")
    print(str(datetime.now()) + ' ' + str(printing))
    log_file.write(str(datetime.now()) + ' ' + str(printing) + '\n')
    log_file.close()
    return logger


def to_latin(text):
    import requests

    url = f"https://korrektor.manu.uz/transliterate?alphabet=latin&text={text}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['result']


# Класс для проверки на изображение (только первая страница)
def check_to_img(file_path):
    reader = PdfReader(file_path)
    image_path = "Pdf2img"
    for page in range(len(reader.pages)):
        logger(f"parsing page {page + 1}")
        try:
            if reader.pages[page].images:
                logger(f"Page {page + 1} has images")
                images = convert_from_path(file_path)
                [image.save(f'{image_path}/Page_{i + 1}.jpg', 'JPEG') for i, image in enumerate(images)]
                result_text = image_to_string(f"{image_path}/Page_{page + 1}.jpg")
                # print(f"result_text: {result_text}")
                if len(result_text) == 0 or result_text == "" or result_text is None:
                    continue
                else:
                    DocumentParser(result_text)
                    logger("page text forwarded to DocumentParser!")
                DocumentReader(file_path, page)
                logger("page text forwarded to DocumentReader 1!")
            else:
                logger(f"Page {page + 1} has no images")
                DocumentReader(file_path, page)
                logger("page text forwarded to DocumentReader 2!")
        # all_text = ''.join(collector_list)
        # DocumentParser(all_text)
        except Exception as e:  # NotImplementedError - если файл сканер, то он не может быть прочитан
            logger(f"Error in check_to_img: {e}")
            continue


class CheckFirstToImg:
    def __init__(self, file_path):
        self.file_path = file_path
        self.check = ''

        check_to_img(self.file_path)


# Класс для чтения pdf файла
class DocumentReader:
    def __init__(self, file_path, page):
        self.text = ''
        self.file_path = file_path
        self.page = page
        self.parts = []

        self.get_coordinates()

    def pdf_convertor(self, x1, y1, x2, y2):
        doc = fitz.open(self.file_path)
        page = doc[self.page]
        # Извлекаем текст из определенной области страницы
        rect = fitz.Rect(x1, y1, x2, y2)

        self.parts.extend(page.get_text("text", clip=rect))

        self.text = ''.join(self.parts)
        self.text = re.sub(r'\s+', ' ', self.text)

        DocumentParser(self.text)

    def get_coordinates(self):
        doc = fitz.open(self.file_path)
        page_coord = doc[self.page]

        # Координаты страницы 1:
        # x1: 0.0, y1: 0.0, x2: 595.3200073242188, y2: 841.9199829101562
        # x1: 0.0, y1: 0.0, x2: 324.0, y2: 515.52001953125
        # Получение координат области страницы
        x1, y1, x2, y2 = page_coord.rect

        self.pdf_convertor(x1=x1, y1=y1 + 12, x2=x2, y2=y2 - 25)


class DocumentParser:
    def __init__(self, text):
        self.text = text
        # функция обрезки текста:
        self.split_text()

    def split_text(self):
        # print(f"split_text: {self.text}")
        replacements = {
            # r"\s+\n\s+": "| ",
            r"\s*-\s*": "-",
            r"\s{2,}": " ",
            r"\s*,\s*": ", ",
            r"\s+»\s+": " ",
            r"» ": " ",
            r"»": "",
            r"\s+»": "",
            r"\s+«\s+": " ",
            r"«\s+": "",
            r"«": "",
            r"\s+—\s+": "—",
            # enters
            r"\n+": " ",
            "\n": " ",
            r"\r+": " ",
            r"\t+": " ",
        }

        # Цикл замены символов
        for pattern, replacement in replacements.items():
            self.text = re.sub(pattern, replacement, self.text)

        # Делим предложения по символам из массива с сохранением знаков препинания ".", "?"
        sentences = re.split(r'(?<=[.?:;])\s+', self.text)

        # print(f"sentences: {sentences}")

        # брать только вопросительные предложения (со знаком "?") из массива предложений иначе - continue
        sentences = [re.split(r'(?<=[.?:;])', sentence) for sentence in sentences]
        lst_sentences = []
        for sentence in sentences:
            for q_sentence in sentence:
                if q_sentence == '' or q_sentence == ' ' or q_sentence == '\n' or q_sentence is None:
                    continue
                elif q_sentence[-1] == '?':
                    lst_sentences.append(q_sentence)
            # if sentence[-1] == '?':
            #     print(f"question sentence: {sentence}")
            #     lst_sentences.append(sentence)
            # else:
            #     continue
        # print(f"last sentences: {lst_sentences}")
        # Записываем, новые предложения, в общий ма ссив.
        new_sentences = [[sentence] for sentence in lst_sentences]
        # print(f"new_sentences: {new_sentences}")
        return self.remove_spaces(new_sentences)

    def remove_spaces(self, sentences):
        remove_spaces_lines = []
        for line_index in range(len(sentences)):  # Индексуем список
            for lines in sentences[line_index]:  # Выводим из списка (str)
                words = lines.split(' ')  # Обрезаем пробелы, отделяем слова друг от друга
                if words[0] == '':  # Если, первый идекс пукстой, то отделяем от массива.
                    self.organize_text(words[1:])
                else:
                    self.organize_text(words)
        # print(f"remove_spaces_lines: {remove_spaces_lines}")
        return remove_spaces_lines

    def organize_text(self, sentences):
        for index, words in enumerate(sentences):
            # TranslateToLatin(words)
            if len(words) == 0 or words == " " or words == "" or words is None:
                continue
            else:
                extended.append(to_latin(words.strip()))


class JoinToStr:
    def __init__(self):
        self.text_list = None
        self.extended_str = ''

    def joined(self):
        try:
            # print(f"JoinToStr: {extended}")
            for a in extended:
                if a is None:
                    continue
                else:
                    self.extended_str += ' ' + ''.join(a)
            return self.extended_str
            # print(f"DocumentSaver: {self.extended_str}")
        except Exception as e:  # Ошибка в индексах (если слово состоит из 1 символа и это не буква)
            if str(e) == "string index out of range":
                self.text_list.append(self.extended_str)
            logger(f"Error in JoinToStr: {e}")


if __name__ == '__main__':
    books_list = os.listdir("books/splitted_book/")
    csv_file = "data/correct_data/questions_sentence.csv"
    for book in sorted(books_list):
        poem_title = os.path.splitext(book)[0]
        files = glob.glob(f'Pdf2img/*')
        for f in files:
            os.remove(f)
        logger(f"{len(files)} old extracted images removed")
        book_path = f"books/splitted_book/{book}"
        logger(f"Book - {book} started!\n")
        parser = CheckFirstToImg(book_path)
        final_text = JoinToStr().joined()
        final_text = re.split(r'(?<=[.?:;])\s+', final_text)
        # print(f"final_text: {final_text}")
        if not os.path.exists(csv_file):
            with open(csv_file, 'w', newline='') as ebook:
                fieldnames = ['Asar_nomi', 'Manbaa', 'Matn']
                writer = csv.DictWriter(ebook, fieldnames=fieldnames, delimiter='|')
                writer.writeheader()
                for new_text in final_text:
                    new_text = new_text.strip().replace("|", "")
                    if new_text == " " or new_text == "" or new_text is None or len(new_text) < 6:
                        continue
                    else:
                        try:
                            result = new_text
                            writer.writerow(
                                {"Asar_nomi": poem_title, "Manbaa": "ziyonet.uz", "Matn": result})
                        except IndexError:
                            writer.writerow(
                                {"Asar_nomi": poem_title, "Manbaa": "ziyonet.uz", "Matn": result})
                        print(f"Book {book} already exists in csv file!")
                        try:
                            os.remove(book_path)
                            logger(f"Book {book} removed from splitted books\n")
                        except FileNotFoundError:
                            print(f"Book {book} already moved from splitted books to done folder!\n")
                            continue
                        continue
            logger(f"Book {book} done successfully!\n")
        else:
            fieldnames = ['Asar_nomi', 'Manbaa', 'Matn']

            # Чтение существующих данных из CSV файла
            existing_data = []
            try:
                with open(csv_file, 'r') as ebook:
                    existing_data = list(csv.DictReader(ebook, delimiter='|'))
            except FileNotFoundError:
                pass  # Если файл не существует, то просто продолжаем

            # Добавление новых данных
            with open(csv_file, 'a', newline='') as ebook:
                writer = csv.DictWriter(ebook, fieldnames=fieldnames, delimiter='|')

                for new_text in final_text:
                    new_text = new_text.strip().replace("|", "")
                    if new_text == " " or new_text == "" or new_text is None or len(new_text) < 6:
                        continue
                    text_exists = any(new_text in existing_text['Matn'] for existing_text in existing_data)
                    title_exists = any(poem_title in existing_title['Asar_nomi'] for existing_title in existing_data)
                    if not text_exists:
                        writer.writerow({"Asar_nomi": poem_title, "Manbaa": "ziyonet.uz", "Matn": new_text})
                    else:
                        print(f"Book {book} already exists in csv file!")
                        try:
                            os.remove(book_path)
                            logger(f"Book {book} removed from splitted books\n")
                        except FileNotFoundError:
                            print(f"Book {book} already moved from splitted books to done folder!\n")
                            continue
                        continue
            logger(f"Book {book} done successfully!\n")
