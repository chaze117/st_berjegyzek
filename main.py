import streamlit as st
import PyPDF2 
import re
from io import BytesIO
import requests
from st_supabase_connection import SupabaseConnection

client = st.connection(name="supabase", type=SupabaseConnection)
def getPDF(link):
    # response = requests.get("https://txwxfzohqokyqsdhbadt.supabase.co/storage/v1/object/sign/berjegyzek/bj.pdf?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJiZXJqZWd5emVrL2JqLnBkZiIsImlhdCI6MTczMzI0NDMwNCwiZXhwIjoyMDQ4NjA0MzA0fQ.oZcBE5-3y1QjlnTLdzEr5pIEfZXld_0npE-bMJAaLgg")
    response = requests.get(link)
    response.raise_for_status()
    if "application/pdf" in response.headers.get("Content-Type", ""):
                pdf_data = BytesIO(response.content)
    return pdf_data

def GetPages(ado,pdf_data):
            object = PyPDF2.PdfReader(pdf_data)
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

bucketfiles = client.list_objects("Berjegyzekek",limit=1000)
files = []
for file in bucketfiles:
      files.append(file['name'])
st.title("Bérjegyzék lekérése")
files.sort(reverse=True)
file = st.selectbox("Hónap kiválasztása:",files)
ado = st.text_input("Adóazonosító")
binary_content = None
if st.button("Bérjegyzék előkészítése") :
    pdflink = client.get_public_url("Berjegyzekek",file)
    pdf = getPDF(pdflink)
    pn = GetPages(ado,pdf)
    extracted_pdf = extract_pdf_pages(pdf, [pn,pn+1])

    st.download_button("Bérjegyzék Letöltése",file_name=ado+'.pdf',data=extracted_pdf)
    
