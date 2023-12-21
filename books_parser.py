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

    url = f"https://korrektor.manu.uz/transliterate?alphabet=latin&{text}"

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
            r"\s+»\s+": "» ",
            r"\s+—\s+": "—",
        }

        # Цикл замены символов
        for pattern, replacement in replacements.items():
            self.text = re.sub(pattern, replacement, self.text)

        # Делим предложения по символам из массива с сохранением знаков препинания.
        sentences = re.split(r"([.?!;])", self.text)
        sentences_with_delimiters = []
        current_sentence = ""
        for token in sentences:
            current_sentence += token
            if token in (".", "!", "?", ";"):
                sentences_with_delimiters.append(current_sentence)
                current_sentence = ""

        # Записываем, новые предложения, в общий массив.
        new_sentences = [[sentence] for sentence in sentences_with_delimiters]
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

        return remove_spaces_lines

    def organize_text(self, sentences):
        for index, words in enumerate(sentences):
            # TranslateToLatin(words)
            if len(words) == 0 or words == " " or words == "" or words is None or len(words) < 6:
                continue
            else:
                # if is_latin_uzbek(words):
                #     extended.append(words.strip())
                # elif is_cyrillic_uzbek(words):
                #     res = TranslateToLatin().split_words(words.strip())
                #     extended.append(res)
                extended.append(to_latin(words.strip()))


# Переводит с кириллицы на латиницу:
# class TranslateToLatin:
#     def __init__(self):
#         self.text_list = []
#         self.list_1 = []
#         self.latin_text_str = ''  # сохраняет переведенный в латиницу текст.
#         self.t = Transliterator(to=WritingType.LAT)  # переводит кириллицу в латиницу
#
#     # Собираем все переведенные слова из списков
#     def sum(self):
#         for sum in self.text_list:
#             self.list_1.extend(self.text_list)
#             return self.list_1
#
#     def split_words(self, word):
#         try:
#             if word == '' or word == [] or len(new_text) < 5:
#                 pass
#             else:
#                 # for word in text:  # Цикл с условием если слово путой str, то это слово пропускают
#                 if word[0].isalpha():  # Если 1 индекс в слове это буква
#                     if word[-1:].isalpha():  # Если последний индекс слова это буква, то слово переводится.
#                         self.text_list.append(self.t.convert(word))
#                     else:  # Если последний индекс слова, не буква, а знак, то:
#                         new_word = f'{self.t.convert(word[:-1])}{word[-1:]}'  # Переводим слово в латиницу, без
#                         # последнего знака и сразу добавляем исключенный знак, после перевода.
#                         self.text_list.append(new_word)
#                 elif not word[0].isalpha() and (not word[0].isdigit()):  # Если 1 индекс это символ
#                     if word[1].isalpha():  # Если 2 индекс это буква
#                         try:
#                             if word[-1:].isalpha:  # Если Последный индекс это буква
#                                 new_word = f'{word[:1]}{self.t.convert(word[1:])}'  # Переводим слово в латиницу, без
#                                 # первого знака и сразу добавляем исключенный знак, после перевода.
#                                 self.text_list.append(new_word)
#                             else:  # Если последний индекс символ
#                                 self.t.convert(word[1:-1])
#                                 new_word = f'{word[:1]}{self.t.convert(word[1:-1])}{word[-1:]}'  # Переводим слово в
#                                 # латиницу, без первого знака и последнего занка, сразу добавляем исключенные знаки,
#                                 # после перевода.
#                                 self.text_list.append(new_word)
#                         except Exception as e:  # При возникновении ошибки: легче сделать так дэ.
#                             new_word = f'{word[:1]}{self.t.convert(word[1:-1])}{word[-1:]}'
#                             self.text_list.append(new_word)
#                             logger(f"Error in split_words: {e}")
#                     else:  # Если первый индекс слова, не буква, то принтуем в терминал,
#                         self.text_list.append(word)
#                 elif word[0].isdigit():  # Если внутри обрезанного слова есть, цифра, то находим цифру и переводим слово
#                     # без нее
#                     collector_list = []  # Для обрезки слов, если в ней есть цифра.
#                     for each_symbol in word:  # Отделяем каждый символ в слове
#                         if each_symbol.isdigit():  # Проверяем, если этот символ цифра, то сохраняем в список коллерктор
#                             collector_list.append(each_symbol)
#                         elif each_symbol.isalpha():  # Если этот символ буква, то переводим букву в латиницу и
#                             # записываем в коллектор переведенную букву.
#                             translated_sym = self.t.convert(each_symbol)
#                             collector_list.append(translated_sym)
#                         else:  # Если этот символ, что-то другое, то добавляем его в коллектор без изменений
#                             collector_list.append(each_symbol)
#                     collector_txt = ''.join(collector_list)  # Перевеодим слово обратно в str
#                     self.text_list.append(collector_txt)  # Добавляем слово в общий список
#         except IndexError as e:  # Ошибка в индексах (если слово состоит из 1 символа и это не буква)
#             if str(e) == "string index out of range":
#                 self.text_list.append(word)
#         return self.sum()


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
    csv_file = "data/correct_data/e-book.csv"
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
        final_text = re.split("[.?!:]", final_text)
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
