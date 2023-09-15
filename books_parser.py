import csv
import re
import os

from PyPDF2 import PdfReader


def path_reader():
    get_files_path = os.listdir('pdf_books')
    files = []
    for get_files in get_files_path:
        files.append(f'pdf_books/{get_files}')
    return files


# path_reader()


# path_reader = "pdf_books/Пиримқул Қодиров Ҳумоюн ва Акбар.pdf"
# reader = PdfReader(path_reader)
parts = []


def visitor_body(pdf_text, cm, tm, fontDict, fontSize):
    y = tm[5]
    if 50 < y < 780:
        parts.append(pdf_text)


def extract_text_from_pdf():
    sentences = []
    for file in path_reader():
        reader = PdfReader(file)
        number_of_pages = len(reader.pages)
        for page in range(number_of_pages):
            page_text = reader.pages[page]
            page_text.extract_text(visitor_text=visitor_body)

        text = ''.join(parts)
        new_splited = re.split("[.?!:]", text.replace(" \n", "").replace("  ", " "))
        sentences.append(new_splited)
    print(sentences)
    return sentences
        # for sentence in sentences:
        #     print(sentence)
        #     print("_________")


def write_to_csv(list_text: list):
    file_exist = 'ebooks.csv'
    for pdf_file in path_reader():
        reader = PdfReader(pdf_file)
        poem_title = reader.pages[0].extract_text(0).split('\n')[0]
        if file_exist:
            with open(file_exist, 'a+', newline='') as ebook:
                fieldnames = ['Asar_nomi', 'Manbaa', 'Matn']
                writers = csv.DictWriter(ebook, fieldnames=fieldnames, delimiter='|')
                writers.writeheader()
                for new_text in list_text:
                    for each_sentence in new_text:
                        if len(each_sentence) == 0:
                            continue
                        else:
                            writers.writerow(
                                {"Asar_nomi": poem_title, "Manbaa": "www.ziyouz.com", "Matn": each_sentence})
        else:
            with open(file_exist, 'a+', newline='') as ebook:
                fieldnames = ['Asar_nomi', 'Manbaa', 'Matn']
                writer = csv.DictWriter(ebook, fieldnames=fieldnames, delimiter='|')
                writer.writeheader()
                for new_text in list_text:
                    for each_sentence in new_text:
                        if len(each_sentence) == 0:
                            continue
                        else:
                            writer.writerow({"Asar_nomi": poem_title, "Manbaa": "www.ziyouz.com", "Matn": new_text})


write_to_csv(extract_text_from_pdf())
