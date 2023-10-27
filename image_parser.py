import glob
import os
import re

from PIL import Image
import pytesseract


# print(pytesseract.image_to_string(Image.open('Page_3.jpg'), lang='uzb',
#                                   config='--tessdata-dir /home/ilyos/Downloads/tessdata_langs/'))
def image_to_string(img_path):
    img = Image.open(img_path)

    x1, y1, x2, y2 = -10, 70, 900, 1300  # X va Y koordinatalarini o'zgartiring
    roi = img.crop((x1, y1, x2, y2))

    result = pytesseract.image_to_string(roi, lang='uzb', config='--tessdata-dir ./tessdata_langs/')

    splitted_list = re.sub(r'\s+', ' ', result)

    splitted_list = re.split(r'(?<=[.!?])\s*', splitted_list)

    for sentence in splitted_list:
        # print(f"Length of sentence: {len(sentence)}"
        #       f"\nSentence: {sentence}\n")
        if len(sentence) == 0 or sentence == '':
            splitted_list.remove(sentence)

    splitted_text = ''.join(splitted_list)

    # print(splitted_text)

    return splitted_text


def all_images_to_string(imgs_path):
    imgs_len = os.listdir(imgs_path)
    collector_list = []
    for i in range(1, len(imgs_len)):
        result_text = image_to_string(f'{imgs_path}/Page_{i}.jpg')
        if len(result_text) == 0 or result_text == "":
            continue
        else:
            collector_list.append(result_text)
        # print(f"Page {i} done successfully!\n")

    all_text = ''.join(collector_list)
    # print(f"final extracted text from images: {all_text}")
    return all_text
