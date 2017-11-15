from io import StringIO

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def convert(fname, pages=None):
    if not pages: #If there are no pages, don't create a set of pages to iterate through (ie just go through them all)
        pagenums = set()
    else: #Otherwise go through these specific pages, don't repeat any pagenumbers
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text

def get_toc(pdf_path):
    infile = open(pdf_path, 'rb')
    parser = PDFParser(infile)
    document = PDFDocument(parser)

    toc = list()
    for (level,title,dest,a,structelem) in document.get_outlines():
        toc.append((level, title))

    return toc

book_text = convert("/Users/Ben/Downloads/Sedgewick_ALGORITHMS_ED4_3513.pdf", range(20))
for c in get_toc("/Users/Ben/Downloads/Sedgewick_ALGORITHMS_ED4_3513.pdf"):
    print((c[0]*"\t")+c[1])
#
# for line in book_text:
#     print(line.strip())
print(book_text)

