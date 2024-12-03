import streamlit as st
import PyPDF2 
import re
from io import BytesIO
output = None
def GetPages(ado):
            object = PyPDF2.PdfReader(r"bj.pdf")
            NumPages = len(object.pages)
            for i in range(0, NumPages):
                PageObj = object.pages[i]
                Text = PageObj.extract_text()
                if re.search(ado,Text):
                    return i
                
def extract_pdf_pages(pdf_file, page_numbers):
    reader = PyPDF2.PdfReader(pdf_file)
    writer = PyPDF2.PdfWriter()
    for page_number in page_numbers:
        writer.add_page(reader.pages[page_number])
    output_pdf = BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf


st.title("Bérjegyzék lekérése")
st.markdown("<h3>Aktuális bérjegyzék: 2024. november</h3>",unsafe_allow_html=True)
ado = st.text_input("Adóazonosító")
binary_content = None
if st.button("Bérjegyzék előkészítése") : 
    pn = GetPages(ado)
    extracted_pdf = extract_pdf_pages("bj.pdf", [pn,pn+1])

    st.download_button("Bérjegyzék Letöltése",file_name=ado+'.pdf',data=extracted_pdf)
    