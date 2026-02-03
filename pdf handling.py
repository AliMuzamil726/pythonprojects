#pdf file read
import PyPDF2
import fpdf

file = open("sample.pdf", "rb")   # rb = read binary
reader = PyPDF2.PdfReader(file)
print(len(reader.pages))  # total pages

#pages text reads

page = reader.pages[1]
text = page.extract_text()
print(text)
file.close()

#read all pages
"""with open("sample.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    
    for page in reader.pages:
        print(page.extract_text())
from PyPDF2 import PdfWriter

writer = PdfWriter()

with open("sample.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    writer.add_page(reader.pages[0])

with open("output.pdf", "wb") as output:
    writer.write(output)"""
#merge pdf
from PyPDF2 import PdfMerger

merger = PdfMerger()
merger.append("sample.pdf")
merger.append("output.pdf")

merger.write("merged.pdf")
merger.close()



