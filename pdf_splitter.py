import glob
import os
from PyPDF2 import PdfReader, PdfWriter


def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfReader(path)

    pdf_page_len = len(pdf.pages)
    pdf_page_size = 10

    for page in range(0, pdf_page_len, pdf_page_size):
        end = min(page + pdf_page_size, pdf_page_len)

        pdf_writer = PdfWriter()
        for page in range(page, end):
            pdf_writer.add_page(pdf.pages[page])

        group_number = (page // pdf_page_size) + 1  # Номер группы

        output_filename = f'books/splitted_book/{fname}_group_{group_number}.pdf'

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        print(f'Created: {output_filename}')


# if __name__ == '__main__':
#     path = 'books/fixed_books/Aleksandr Pushkin. Kapitan qizi_fixed.pdf'
#     pdf_splitter(path)
