# import re
#
# from PyPDF2 import PdfReader
#
# reader = PdfReader("pdf_books/Пиримқул Қодиров Ҳумоюн ва Акбар.pdf")
# path_reader = "pdf_books/Пиримқул Қодиров Ҳумоюн ва Акбар.pdf"
# stop_words = ['www', 'ziyouz', 'com', 'кутубхонаси', '_____________', '*']
#
#
# def extracted_func():
#     number_of_pages = len(reader.pages)
#
#     extracted_text = []
#     # text = reader.pages[0]
#     # extracted = text.extract_text(0).replace("\n", '')
#     # splited_text = re.split("[.!:?\n]", extracted)
#     # print('splited_text', splited_text)
#     # for s in splited_text:
#     #     if s not in stop_words:
#     #         print(f"not in stop words: {s}")
#     #     else:
#     #         print(f"in stop words: {s}")
#     for page in range(number_of_pages):
#         text = reader.pages[page]
#         extracted = text.extract_text(0).replace("\n", '')
#         splited_text = re.split("[.?!:]", extracted)
#         extracted_text.append(splited_text)
#
#     return extracted_text
#
#
# # extracted_func()
#
#
# def write_to_csv(list_text: list):
#     file_exist = 'ebooks.csv'
#     poem_title = reader.pages[0].extract_text(0).split('\n')[0]
#     # if file_exist:
#     #     with open(file_exist, 'a+', newline='') as ebook:
#     #         fieldnames = ['asar_nomi', 'manbaa', 'matn']
#     #         writers = csv.DictWriter(ebook, fieldnames=fieldnames, delimiter='|')
#     for text in list_text:
#         print('text', text)
#         for word in text:
#             print("word", word)
#             if word not in stop_words:
#                 print('stop words', word)
#                 # writers.writerow({"asar_nomi": poem_title, "manbaa": "www.ziyouz.com", "matn": word})
#             else:
#                 break
#     # elif not file_exist:
#     #     with open(file_exist, 'a+', newline='') as ebook:
#     #         fieldnames = ['asar_nomi', 'manbaa', 'matn']
#     #         writer = csv.DictWriter(ebook, fieldnames=fieldnames, delimiter='|')
#     #         writer.writeheader()
#     #         for text in list_text:
#     #             for word in text:
#     #                 if word not in stop_words:
#     #                     writer.writerow({"asar_nomi": poem_title, "manbaa": "www.ziyouz.com", "matn": word})
#     #                 else:
#     #                     break
#
#
# # write_to_csv(extracted_func())
#
#
# """ xozircha eng ma'qul va qo'yilgan talabga yaqin variant """
# parts = []
#
#
# def visitor_body(text, cm, tm, fontDict, fontSize):
#     y = tm[5]
#     if y > 50 and y < 780:
#         parts.append(text)
#
#
# def extract_text_from_pdf():
#     number_of_pages = len(reader.pages)
#     # page = reader.pages[4]
#     for page in range(number_of_pages):
#         page_text = reader.pages[page]
#         page_text.extract_text(visitor_text=visitor_body)
#         text_body = "".join(parts)
#     return text_body
#
#
# print(extract_text_from_pdf())



