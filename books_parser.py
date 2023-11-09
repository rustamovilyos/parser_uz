import datetime
import glob
import os
import re

from PyPDF2 import PdfReader
from fitrat import Transliterator, WritingType
import csv

from pdf2image import convert_from_path

from image_parser import all_images_to_string, image_to_string
from pdf_splitter import pdf_splitter

extended = []


def is_latin_uzbek(text):
    latin_uzbek_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for char in text:
        if char in latin_uzbek_letters:
            return True
        else:
            return False


def is_cyrillic_uzbek(text):
    cyrillic_uzbek_letters = "абвгғдеёжзийкқлмнопрстуфхцчшъыьэюяҳАБВГҒДЕЁЖЗИЙКҚЛМНОПРСТУФХЦЧШЪЫЬЭЮЯҲ"
    for char in text:
        if char in cyrillic_uzbek_letters:
            return True
        else:
            return False


# Класс для проверки на изображение (только первая страница)
def check_to_img(file_path):
    reader = PdfReader(file_path)
    image_path = "Pdf2img"
    collector_list = []
    try:
        for page in range(len(reader.pages)):
            print(f"parsing page {page + 1}")
            if reader.pages[page].images:
                print(f"Page {page + 1} has images")
                images = convert_from_path(file_path)
                [image.save(f'{image_path}/Page_{i + 1}.jpg', 'JPEG') for i, image in enumerate(images)]
                result_text = image_to_string(f"{image_path}/Page_{page + 1}.jpg")
                # print(f"result_text: {result_text}")
                if len(result_text) == 0 or result_text == "" or result_text is None:
                    print(f"Page {page + 1} has no text")
                    continue
                else:
                    # collector_list.append(result_text)
                    DocumentParser(result_text)
                    print("page text forwarded to DocumentParser")
                # print(f"Page {page + 1} has images")
                DocumentReader(reader.pages[page])
                print("page text forwarded to DocumentReader")
            else:
                print(f"Page {page + 1} has no images")
                DocumentReader(reader.pages[page])
                print("page text forwarded to DocumentReader 2!")
        # all_text = ''.join(collector_list)
        # DocumentParser(all_text)
    except Exception as e:
        print(e)


class CheckFirstToImg:
    def __init__(self, file_path):
        self.file_path = file_path
        # print(f"CheckFirstToImg: {self.file_path}")
        self.check = ''

        check_to_img(self.file_path)


# Класс для чтения pdf файла
class DocumentReader:
    def __init__(self, content):
        self.text = None
        self.content = content
        self.parts = []

        self.extract_text_from_pdf()

    def visitor_body(self, pdf_text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if 50 < y < 780:
            self.parts.append(pdf_text)  # Построчное чтение pdf файла.

    def extract_text_from_pdf(self):
        self.content.extract_text(visitor_text=self.visitor_body)
        self.text = ''.join(self.parts)

        # Запуск функции парсера
        DocumentParser(self.text)
        # print(f"extract_text_from_pdf: {self.text}")


class DocumentParser:
    def __init__(self, text):
        self.text = text
        # print(f"DocumentParser: {self.text}\n\n")
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
        # print(f"removed sentences: {self.remove_spaces(new_sentences)}")
        return self.remove_spaces(new_sentences)

        # print(new_sentences)

    def remove_spaces(self, sentences):
        remove_spaces_lines = []
        # print(f"remove_spaces: {len(sentences)}")
        for line_index in range(len(sentences)):  # Индексуем список
            # print(f"remove_spaces_line_index: {line_index}")
            for lines in sentences[line_index]:  # Выводим из списка (str)
                # print(f"remove_spaces_lines: {lines}")
                words = lines.split(' ')  # Обрезаем пробелы, отделяем слова друг от друга
                # print(f"remove_spaces_words: {words}")
                if words[0] == '':  # Если, первый идекс пукстой, то отделяем от массива.
                    self.organize_text(words[1:])
                else:
                    self.organize_text(words)

        return remove_spaces_lines

    def organize_text(self, sentences):
        for index, words in enumerate(sentences):
            # TranslateToLatin(words)
            if len(words) == 0 or words == " " or words == "" or words is None:
                continue
            else:
                if is_latin_uzbek(words):
                    # print("Text is already in latin")
                    extended.append(words.strip())
                elif is_cyrillic_uzbek(words):
                    # print("Text is in cyrillic")
                    res = TranslateToLatin().split_words(words.strip())
                    extended.append(res)

        # return res


# Переводит с кириллицы на латиницу:
class TranslateToLatin:
    def __init__(self):
        self.text_list = []
        self.list_1 = []
        self.latin_text_str = ''  # сохраняет переведенный в латиницу текст.
        self.t = Transliterator(to=WritingType.LAT)  # переводит кириллицу в латиницу

    # Собираем все переведенные слова из списков
    def sum(self):
        for sum in self.text_list:
            self.list_1.extend(self.text_list)
            return self.list_1

    def split_words(self, word):
        try:
            if word == '' or word == [] or len(word) == 0:
                pass
            else:
                # for word in text:  # Цикл с условием если слово путой str, то это слово пропускают
                if word[0].isalpha():  # Если 1 индекс в слове это буква
                    if word[-1:].isalpha():  # Если последний индекс слова это буква, то слово переводится.
                        self.text_list.append(self.t.convert(word))
                    else:  # Если последний индекс слова, не буква, а знак, то:
                        new_word = f'{self.t.convert(word[:-1])}{word[-1:]}'  # Переводим слово в латиницу, без
                        # последнего знака и сразу добавляем исключенный знак, после перевода.
                        self.text_list.append(new_word)
                elif not word[0].isalpha() and (not word[0].isdigit()):  # Если 1 индекс это символ
                    if word[1].isalpha():  # Если 2 индекс это буква
                        try:
                            if word[-1:].isalpha:  # Если Последный индекс это буква
                                new_word = f'{word[:1]}{self.t.convert(word[1:])}'  # Переводим слово в латиницу, без
                                # первого знака и сразу добавляем исключенный знак, после перевода.
                                self.text_list.append(new_word)
                            else:  # Если последний индекс символ
                                self.t.convert(word[1:-1])
                                new_word = f'{word[:1]}{self.t.convert(word[1:-1])}{word[-1:]}'  # Переводим слово в
                                # латиницу, без первого знака и последнего занка, сразу добавляем исключенные знаки,
                                # после перевода.
                                self.text_list.append(new_word)
                        except Exception as e:  # При возникновении ошибки: легче сделать так дэ.
                            new_word = f'{word[:1]}{self.t.convert(word[1:-1])}{word[-1:]}'
                            self.text_list.append(new_word)
                    else:  # Если первый индекс слова, не буква, то принтуем в терминал,
                        self.text_list.append(word)
                elif word[0].isdigit():  # Если внутри обрезанного слова есть, цифра, то находим цифру и переводим слово
                    # без нее
                    collector_list = []  # Для обрезки слов, если в ней есть цифра.
                    for each_symbol in word:  # Отделяем каждый символ в слове
                        if each_symbol.isdigit():  # Проверяем, если этот символ цифра, то сохраняем в список коллерктор
                            collector_list.append(each_symbol)
                        elif each_symbol.isalpha():  # Если этот символ буква, то переводим букву в латиницу и
                            # записываем в коллектор переведенную букву.
                            translated_sym = self.t.convert(each_symbol)
                            collector_list.append(translated_sym)
                        else:  # Если этот символ что то другое, то добавляем его в коллектор без изменений
                            collector_list.append(each_symbol)
                    collector_txt = ''.join(collector_list)  # Перевеодим слово обратно в str
                    self.text_list.append(collector_txt)  # Добавляем слово в общий список
        except IndexError as e:  # Ошибка в индексах (если слово состоит из 1 символа и это не буква)
            if str(e) == "string index out of range":
                self.text_list.append(word)
        return self.sum()


class JoinToStr:
    def __init__(self):
        self.text_list = None
        self.extended_str = ''

    def joined(self):
        # newlist = []
        # extended.clear()
        try:
            # print(f"JoinToStr: {extended}")
            for a in extended:
                if a is None:
                    continue
                else:
                    self.extended_str += ' ' + ''.join(a)
            #
            # DocumentSaver(self.extended_str)
            return self.extended_str
            # print(f"DocumentSaver: {self.extended_str}")
        except Exception as e:  # Ошибка в индексах (если слово состоит из 1 символа и это не буква)
            if str(e) == "string index out of range":
                self.text_list.append(self.extended_str)
            print(e)


if __name__ == '__main__':
    # Запуск с класса Проверки на изображение
    fixed_books = os.listdir("books/fixed_books/")
    books_list = os.listdir("books/splitted_book/")
    processed_books = set()
    csv_file = "data/e-book.csv"
    for book in sorted(books_list):
        poem_title = os.path.splitext(book)[0]
        files = glob.glob(f'Pdf2img/*')
        for f in files:
            os.remove(f)
        print(len(files), "old extracted images removed")
        book_path = f"books/splitted_book/{book}"
        print(f"Book {book} started!\n")
        parser = CheckFirstToImg(book_path)
        final_text = JoinToStr().joined()
        final_text = re.split("[.?!:]", final_text)
        # print(f"\nfinal text: {final_text}\n\n")
        if not os.path.exists(csv_file):
            with open(csv_file, 'w', newline='') as ebook:
                fieldnames = ['Asar_nomi', 'Manbaa', 'Matn']
                writer = csv.DictWriter(ebook, fieldnames=fieldnames, delimiter='|')
                writer.writeheader()
                for new_text in final_text:
                    new_text = new_text.strip().replace("|", "")
                    print(f"new_text: {new_text}")
                    if len(new_text) == 0 or new_text == " " or new_text == "" or new_text is None:
                        continue
                    else:
                        try:
                            result = new_text
                            writer.writerow(
                                {"Asar_nomi": poem_title, "Manbaa": "www.ziyouz.com", "Matn": result})
                            # print(f"else 1 done {result}")
                        except IndexError:
                            writer.writerow(
                                {"Asar_nomi": poem_title, "Manbaa": "www.ziyouz.com", "Matn": result})
                            # print(f"else 2 done {result}")
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
                    if len(new_text) == 0 or new_text == " " or new_text == "" or new_text is None:
                        continue

                    # Проверка, что новый текст не существует в существующих данных
                    text_exists = any(new_text in existing_text['Matn'] for existing_text in existing_data)

                    if not text_exists:
                        writer.writerow({"Asar_nomi": poem_title, "Manbaa": "www.ziyouz.com", "Matn": new_text})
        print(f"{datetime.datetime.now()} - Book {book} done successfully!\n")
    # except Exception as e:
    #     print(e)
