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
import os

books_list = os.listdir('books/fixed_books')
for i in range(len(books_list)):
    poem_title = os.path.basename(books_list[i][:-4])

    print(poem_title)
