import glob
import os
import shutil
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


# pdf2img2txt("books/scanned_books/Михаил Лермантов Замонамиз қаҳрамони.pdf")

def check_to_img(file_path):
    reader = PdfReader(file_path)
    for page in range(len(reader.pages)):
        print(f"checking to image {page}")
        if reader.pages[page].images:
            print(f"Page {page + 1} has images")
            # return pdf2img2txt(file_path)
        else:
            print(f"Page {page + 1} has no images")


def sort_pdf(input_pdf):
    reader = PdfReader("books/renamed_books/" + input_pdf)
    try:
        print(f"Checking {input_pdf} file to images")
        if reader.pages[3].images:
            print(f"PDF file {input_pdf} has images, but it is not scanned")
            shutil.move(f"books/renamed_books/{input_pdf}", "books/fixed_images")
            print(f"PDF {input_pdf} file with images is moved to fixed_books folder\n\n")
        else:
            shutil.move(f"books/renamed_books/{input_pdf}", "books/books_to_parse")
            print(f"PDF {input_pdf} file has no images")
            print(f"PDF {input_pdf} file is moved to fixed_books folder\n\n")
    except NotImplementedError:
        print("NotImplementedError")
        shutil.move(f"books/renamed_books/{input_pdf}", "books/scanned_books")
        print(f"PDF {input_pdf} file is scanned and moved to scanned_books folder\n\n")


# sort_pdf('books/renamed_books/Ов.pdf')

# for pdf_book in sorted(os.listdir('books/renamed_books')):
#     sort_pdf(pdf_book)


def scan_pdf_fixer(input_pdf):
    output_pdf = os.path.basename(input_pdf)[:-4] + ".pdf"
    output_pdf_1 = f'books/fixed_books/{output_pdf}'
    print(f"Output file: {output_pdf_1}")

    # Команда Ghostscript для обработки PDF файла и создания нового
    # gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER  -sOutputFile=output.pdf input.pdf
    command = ["gs", "-sDEVICE=pdfwrite", "-dNOPAUSE", "-dBATCH", "-dSAFER", f"-sOutputFile={output_pdf_1}", input_pdf]

    # Вызов команды Ghostscript
    subprocess.run(command, capture_output=True, text=True)
    print("PDF file has been fixed")


# scan_pdf_fixer("books/books_to_parse/Ikki eshik orasi.pdf")

# for pdf_book in glob.glob('books/splitted_book/*.pdf'):
#     scan_pdf_fixer(pdf_book)
