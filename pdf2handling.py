import fpdf #Used for Create a pdf
#import PyPDF2 # used for merge,read and split pdf
"""f= open("sample.pdf","rb")
reader = PyPDF2.PdfReader(f)
print(reader.pages[1].extract_text())
#multiple or all pages read
f= open("sample.pdf","rb")
reader = PyPDF2.PdfReader(f)
for page in reader.pages:
    print(page.extract_text())"""
from PyPDF2 import PdfReader,PdfWriter,PdfMerger
#spilt pdf
"""read=PdfReader("sample.pdf")
write=PdfWriter()
write.add_page(read.pages[1])
with open("sample.pdf","wb") as f:
    write.write(f)"""
#merge pdf 
merger=PdfMerger()
merger.append("sample.pdf")
merger.append("sample1.pdf")
merger.write("merged.pdf")
merger.close()







