import os
import subprocess

from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from image_parser import all_images_to_string


def pdf2img2txt(pdf_path):
    # Convert PDF to a list of image objects
    images = convert_from_path(pdf_path)
    images_path = 'Pdf2img'
    # Loop through the images and save them
    for i, image in enumerate(images):
        if os.path.exists(f"{images_path}/Page_{i + 1}.jpg', 'JPEG'"):
            print(f"Page {i + 1} already exists")
            break
        else:
            image.save(f'{images_path}/Page_{i + 1}.jpg', 'JPEG')
        print(f"Page {i + 1} was saved successfully as Page_{i + 1}.jpg\n")

    return all_images_to_string(images_path)


# pdf2img2txt('books/fixed_books/Одил Ёқубов Улуғбек ҳазинаси-1-6_fixed.pdf')

def check_to_img(file_path):
    reader = PdfReader(file_path)
    for page in range(len(reader.pages)):
        print(f"checking to image {page}")
        if reader.pages[page].images:
            print(f"Page {page + 1} has images")
            # return pdf2img2txt(file_path)
        else:
            print(f"Page {page + 1} has no images")


def pdf_fixer(input_pdf):
    # Имя выходного файла
    output_pdf = os.path.basename(input_pdf[:-4]) + "_fixed.pdf"
    output_pdf_1 = f'books/fixed_books/{output_pdf}'
    print(f"Output file: {output_pdf_1}")

    # Команда Ghostscript для обработки PDF файла и создания нового
    # gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER  -sOutputFile=output.pdf input.pdf
    command = ["gs", "-sDEVICE=pdfwrite", "-dNOPAUSE", "-dBATCH", "-dSAFER", f"-sOutputFile={output_pdf_1}", input_pdf]

    # Вызов команды Ghostscript
    subprocess.run(command, capture_output=True, text=True)
    print("PDF file has been fixed")


# pdf_fixer('books/renamed_books/Ов.pdf')

# for pdf_book in glob.glob("books/renamed_books/*"):
#     pdf_fixer(pdf_book)
