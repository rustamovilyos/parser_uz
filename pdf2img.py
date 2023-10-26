from pdf2image import convert_from_path
from image_parser import all_images_to_string


def pdf2img2txt(pdf_path):
    # Convert PDF to a list of image objects
    images = convert_from_path(pdf_path)
    images_path = 'Pdf2img'
    # Loop through the images and save them
    for i, image in enumerate(images):
        image.save(f'{images_path}/Page_{i + 1}.jpg', 'JPEG')
        print(f"Page {i + 1} was saved successfully as Page_{i + 1}.jpg\n")

    return all_images_to_string(images_path)


# if __name__ == '__main__':
#     run = pdf_to_img('books/Одил Ёқубов Улуғбек ҳазинаси.pdf')
#     print(run)
