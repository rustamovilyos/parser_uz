# from PIL import Image
# import pytesseract
#
# # Transforming image to string and printing it!
# # for i in range(1, 4):
# #     print(pytesseract.image_to_string(Image.open('Page_{}.jpg'.format(i)), lang='uzb',
# #                                       config='--tessdata-dir /home/ilyos/Downloads/tessdata_langs/'))
#
# # print(pytesseract.image_to_string(Image.open('Page_3.jpg'), lang='uzb',
# #                                   config='--tessdata-dir /home/ilyos/Downloads/tessdata_langs/'))
#
# # Suratni yuklab olamiz
# img = Image.open('Page_3.jpg')
#
# # Qirqib olish uchun qattiqni aniqlash
# x1, y1, x2, y2 = -10, 580, 7000, 2300  # X va Y koordinatalarini o'zgartiring
# roi = img.crop((x1, y1, x2, y2))
#
# # Qirqib olingan qattiqni o'qib olish
# result = pytesseract.image_to_string(roi, lang='uzb', config='--tessdata-dir /home/ilyos/Downloads/tessdata_langs/')
#
# print(result)
# import ast
# import json
#
# # data = '{"key": 10, "key2": [1,2,3], "array": array([0., 0., 0., 0., 0., 0.], dtype=float32)}'
# # a = data[:27] + '}'
# # b = '{' + data[29:]
# # print(ast.literal_eval(a))
# # print(ast.literal_eval(b))
# # print(data)
# # convert string to dictionary
# # data_1 = dict(data)
# # using json.loads()
# # data_2 = json.loads(data[-4:])
# # print(data_2)
# # using ast.literal_eval()
# # data_3 = ast.literal_eval(data)
# # print(data_3)
# # d = {}
# # print(data.split(','))
#
# import ast
#
# data = ("{'path': '/mnt/SSD-01/tts-training/S2T/muxlisa-uz/dataset/clips/common_voice_uz_29166029.mp3',"
#         " 'array': array([0., 0., 0., ..., 0., 0., 0.]), 'sampling_rate': 32000}")
# dict1 = ast.literal_eval(data)
#
# print(dict1)
import csv
import glob
import os


# import os
#
# # import os
# #
# # books_list = os.listdir('books/fixed_books')
# # for i in range(len(books_list)):
# #     poem_title = os.path.basename(books_list[i][:-4])
# #
# #     print(poem_title)
#
#
# # split pdf files into pages
# # pdf_splitter.py
#
# o = os.listdir('books/splitted_book')
# if "s" in o:
#     print("in")
# print("out")
# print(" fe".strip())
# from PyPDF2 import PdfReader
#
# pdf = PdfReader('books/splitted_book/Abdulla Qodiriy - Mehrobdan chayon_fixed_group_14.pdf')
#
# for i in range(len(pdf.pages)):
#     text = pdf.pages[i].extract_text().replace('\n', '')
#     print(text)

# import fitz  # PyMuPDF
#
# pdf_document = "books/splitted_book/Abdulla Qodiriy - Mehrobdan chayon_fixed_group_14.pdf"
# pdf = fitz.open(pdf_document)
#
# for page_number in range(len(pdf)):
#     page = pdf.load_page(page_number)
#
#     text = page.get_page_images()
#
#     # text = text.replace('\n', ' ').replace('\x0c', '')  # Заменяем символы новой строки и форм-фид на пробел
#     print(text)

# pdf.close()
# ----------------------------------------------------------------------------------------------------------
# import csv
# #
# csv_file = 'data/e-book.csv'
# books_list = os.listdir("books/splitted_book/")
# exists_books = []
# not_exists_books = []
# for book in sorted(books_list):
#     poem_title = os.path.splitext(book)[0]
#     # new_text = "mistеr Xolms, mеn yurimsak emasman, ish kеtidan quvmayman, ish o’zi mеni qidirib kеladigan bo’lgani
#     # uchun ba'zan haftalab ostona hatlab ko’chaga chiqmayman"
#     if csv_file:
#         with open(csv_file, 'r') as ebook:
#             existing_data = list(csv.DictReader(ebook, delimiter='|'))
#             # text_exists = any(new_text in existing_text['Matn'] for existing_text in existing_data)
#             existing_title = any(poem_title in existing_title['Asar_nomi'] for existing_title in existing_data)
#             if existing_title:
#                 print(f"\n\nBook already exists in csv file!")
#                 print(f"Book: {poem_title}")
#                 exists_books.append(poem_title)
#
#                 pass
#             else:
#                 print("\n\nBook does not exist in csv file!")
#                 print(f"Book: {poem_title}")
#                 not_exists_books.append(poem_title)
#
#                 pass
# print(f"Exists books: {len(exists_books)}")
# print(f"Not exists books: {len(not_exists_books)}")

# book = "books/splitted_book/А.Навоий. Ғазал гулзоридан 100 оташин гул_fixed_group_4.pdf"
# poem_title = os.path.splitext(book)
#
# print(poem_title)

# books = os.listdir("books/splitted_book/")
# for book in sorted(books):
#     print(book)
# poem_title = os.path.splitext(book)[0]
# print(poem_title)

# b = 'books/splitted_book/А.Навоий. Ғазал гулзоридан 100 оташин гул_fixed_group_4.pdf'
#
# print(os.path.basename(b)[:-4])

# with open("dataset_3363_4 (2).txt", 'r') as reader, open("mid.txt", 'w') as writer:
#     reader = reader.read().replace("\n", ';').split(";")
#     result_dict = {}
#     current_key = None
#     student_mid = []
#     # sum_list = []
#     a = ''
#     for item in reader:
#         if item.isalpha():
#             current_key = item
#             result_dict[current_key] = []
#         elif current_key is not None:
#             result_dict[current_key].append(int(item))
#     for key, value in result_dict.items():
#         student_mid.append(sum(value) / 3)
#     for i in student_mid:
#         writer.write(str(i) + '\n')
#
#     sum_list = [0] * len(result_dict[key])
#
#     # Sum the corresponding elements at each index
#     for key, value in result_dict.items():
#         average_score = sum(value[0:3]) / 3
#         # sum_list =
#
#     writer.write(str(sum_list) + ' ')
    # for i in sum_list:

    # writer.write(str(a / 3) + " ")

# import this
# print("Hello world from Python")
