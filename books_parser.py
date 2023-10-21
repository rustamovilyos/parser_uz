import os
import re
from PyPDF2 import PdfReader
from fitrat import Transliterator, WritingType
import csv

extended = []


# Класс для проверки на изображение (только первая страница)
def check_to_img(file_path):
    reader = PdfReader(file_path)
    try:
        for page in range(len(reader.pages)):
            print(f"checking to image {page}")
            if reader.pages[page].images:
                print(f"Page {page + 1} has images")
                DocumentReader(reader.pages[page])
            else:
                print(f"Page {page + 1} has no images")
                DocumentReader(reader.pages[page])
    except Exception as e:
        print(e)


class CheckFirstToImg:
    def __init__(self, file_path):
        self.file_path = file_path
        print(f"CheckFirstToImg: {self.file_path}")
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


def organize_text(sentences):
    for index, words in enumerate(sentences):
        # TranslateToLatin(words)
        res = TranslateToLatin().split_words(words)
        extended.append(res)
        # print(f"organize_text: {res}")
    return extended


def remove_spaces(sentences):
    # print(f"remove_spaces: {len(sentences)}")
    remove_spaces_lines = []
    for line_index in range(len(sentences)):  # Индексуем список
        # print(f"remove_spaces_line_index: {line_index}")
        for lines in sentences[line_index]:  # Выводим из списка (str)
            # print(f"remove_spaces_lines: {lines}")
            words = lines.split(' ')  # Обрезаем пробелы, отделяем слова друг от друга
            # print(f"remove_spaces_words: {words}")
            if words[0] == '':  # Если, первый идекс пукстой, то отделяем от массива.
                without_empty_sen = organize_text(words[1:])
                for a in without_empty_sen:
                    if a not in remove_spaces_lines:
                        remove_spaces_lines.append(without_empty_sen)
            else:
                sen = organize_text(words)
                for a in sen:
                    if a not in remove_spaces_lines:
                        remove_spaces_lines.append(sen)

    # Дорабатываем исправление текста внутри массива, добавляем искоючение if, elif, else:
    # print(f"remove_spaces_lines: {remove_spaces_lines}")


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
        # print(f"removed sentences: {remove_spaces(new_sentences)}")
        return remove_spaces(new_sentences)
        # print(new_sentences)

        # Исправление и упорядочение текста внутри массива new_sentences, что бы избежать ошибок.


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

    def joinded(self):
        # newlist = []
        try:
            self.extended_str = ' '.join(' '.join(l) for l in extended)
            # print(self.extended_str)
            # for i in self.extended_str:
            #   self.newlist = self.extended_str.split('|')
            #   # self.newlist.append(i)
            # print(self.newlist)

            DocumentSaver(self.extended_str)
        except Exception as e:  # Ошибка в индексах (если слово состоит из 1 символа и это не буква)
            if str(e) == "string index out of range":
                self.text_list.append(self.extended_str)


# Класс сохранения в csv формате.
def write_to_csv(list_text: list):
    reader = PdfReader("books/Ҳумоюн ва Акбар – Авлодлар довони (роман). Пиримқул Қодиров.pdf")
    check_file_exist = os.path.exists("data/e-book.csv")
    file_for_write = "data/e-book.csv"
    poem_title = reader.pages[0].extract_text(0).split('\n')[0]
    # print(list_text)

    if check_file_exist:
        with open(file_for_write, 'a+', newline='') as ebook:
            fieldnames = ['Asar_nomi', 'Manbaa', 'Matn']
            writers = csv.DictWriter(ebook, fieldnames=fieldnames, delimiter='|')
            writers.writeheader()

            for new_text in list_text:
                if len(new_text) == 0 or new_text == " " or new_text == "":
                    continue
                # for each_sentence in new_text:
                #   print(each_sentence)
                #   if not each_sentence:
                #     continue
                else:
                    try:
                        result = new_text
                        writers.writerow({"Asar_nomi": poem_title, "Manbaa": "www.ziyouz.com", "Matn": result})
                        # print(result)
                    except IndexError:
                        writers.writerow({"Asar_nomi": poem_title, "Manbaa": "www.ziyouz.com", "Matn": result})
    else:
        # print(list_text)
        with open(file_for_write, 'a+', newline='') as ebook:
            fieldnames = ['Asar_nomi', 'Manbaa', 'Matn']
            writer = csv.DictWriter(ebook, fieldnames=fieldnames, delimiter='|')
            writer.writeheader()
            for new_text in list_text:
                if len(new_text) == 0 or new_text == " " or new_text == "":
                    continue
                # for each_sentence in new_text:
                #   if not each_sentence:
                #     continue
                else:
                    try:
                        result = new_text
                        # print(result)
                        writer.writerow({"Asar_nomi": poem_title, "Manbaa": "www.ziyouz.com", "Matn": result})
                    except IndexError:
                        writer.writerow({"Asar_nomi": poem_title, "Manbaa": "www.ziyouz.com", "Matn": result})


class DocumentSaver:
    def __init__(self, text_list):
        self.text_list = re.split("[.?!:]", text_list)
        # print(f"\n\n\nDocumentSaver: {self.text_list}\n\n\n")
        write_to_csv(self.text_list)


if __name__ == '__main__':
    # Запуск с класса Проверки на изображение
    book_path = "books/Ҳумоюн ва Акбар – Авлодлар довони (роман). Пиримқул Қодиров-1-4.pdf"
    # second_file_path = "Alisher Navoiy. Badoyi' ul-bidoya-1-2.pdf"
    parser = CheckFirstToImg(book_path)
    # second_parser = CheckFirstToImg(second_file_path)
    JoinToStr().joinded()
