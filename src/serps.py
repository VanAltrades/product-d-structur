import numpy as np
import os
import advertools as adv
import requests
import PyPDF2
# import fitz

from .config_secrets import SE_API_KEY, SE_ID
# from Product import Product

def get_serp(query):

    serp = adv.serp_goog(q=[query], key=SE_API_KEY, cx=SE_ID)
    return serp

def get_serp_brand_mpn(self):

    query = f"{self._brand} {self._mpn}"
    serp = adv.serp_goog(q=[query], key=SE_API_KEY, cx=SE_ID)
    return serp

def get_serp_pdfs(self):
    """
    Returns a dictionary of PDFs {name:link} related to a product's brand/mpn.
    """
    query = f"filetype:pdf {self._brand} {self._mpn} product information"
    serp = adv.serp_goog(q=[query], key=SE_API_KEY, cx=SE_ID)

    pdf_rank = list(serp['rank'])
    pdf_links = list(serp['link'])
    pdf_links_names = [link.split('.pdf')[0].rsplit('/',1)[1] for link in pdf_links] 
    pdf_names = []
    for rank,name in zip(pdf_rank,pdf_links_names):
        pdf_file_name = f"{self._brand}_{self._mpn}_{str(rank)}_{name}.pdf"
        pdf_file_name = pdf_file_name.replace(' ','_')
        pdf_file_name = pdf_file_name.replace('(','')
        pdf_file_name = pdf_file_name.replace(')','')
        pdf_file_name = pdf_file_name.replace('%','')
        pdf_file_name = pdf_file_name.replace('#','')
        pdf_names.append(pdf_file_name)

    pdf_dict = {name: link for name, link in zip(pdf_names, pdf_links)}
    self._pdfs = pdf_dict

def get_pdf_relevance_score():
    """
    # TODO: In a future state it will be helpful to add information to the _pdfs dict 
            that returns a confidence score from 0 to 1 that explains how relevant a pdf is to the product.
    """
    return

def download_pdfs(self, pdfs_path = "../data/pdfs"):
    """
    Downloads pdf links to a directory called pdfs_path using a given name.
    Run self.get_serp_pdfs() before running download_pdfs() to initialize the list of pdfs.
    """
    for pdf_name, pdf_link in self._pdfs.items():
        print(pdf_name, pdf_link)
        # define exact path to save the pdf in the loop
        pdf_file_path = f"{pdfs_path}/{pdf_name}"
        print(pdf_file_path)

        response = requests.get(pdf_link)

        if response.status_code == 200:
            pdf_content = response.content
            pdf_file_path = os.path.join(pdfs_path, pdf_name)

            with open(pdf_file_path, 'wb') as pdf_file:
                pdf_file.write(pdf_content)
                print(f"PDF downloaded and saved as '{pdf_file_path}'")
        else:
            print(f"Failed to download PDF. Status code: {response.status_code}")

@staticmethod
def extract_pdf_text(source_directory = '../data/pdfs', target_directory = '../data/pdf_text'):

    for filename in os.listdir(source_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(source_directory, filename)
            
            # Open PDF file
            pdf_file = open(pdf_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Close PDF file
            pdf_file.close()
            
            # Save extracted text to a text file in the target directory
            target_filename = os.path.splitext(filename)[0] + '.txt'
            target_path = os.path.join(target_directory, target_filename)
            with open(target_path, 'w', encoding='utf-8') as target_file:
                target_file.write(text)
            
            print(f'Extracted text from {filename} and saved to {target_filename}')

# @staticmethod
# def extract_pdf_images(source_directory = '../data/pdfs', target_directory = '../data/pdf_images'):

#     for filename in os.listdir(source_directory):
#         if filename.endswith('.pdf'):
#             pdf_path = os.path.join(source_directory, filename)
            
#             # Open PDF file
#             pdf_document = fitz.open(pdf_path)
            
#             # Iterate through pages and extract images
#             for page_number in range(pdf_document.page_count):
#                 page = pdf_document[page_number]
#                 images = page.get_images(full=True)
                
#                 for img_index, img in enumerate(images):
#                     xref = img[0]
#                     base_image = pdf_document.extract_image(xref)
#                     image_data = base_image["image"]
#                     image_filename = f'{filename}_page_{page_number + 1}_image_{img_index + 1}.png'
#                     image_path = os.path.join(target_directory, image_filename)
                    
#                     with open(image_path, 'wb') as image_file:
#                         image_file.write(image_data)
                    
#                     print(f'Image extracted from {filename} and saved as {image_filename}')
            
#             # Close PDF file
#             pdf_document.close()

# @staticmethod
# # pip install tabula-py
# # import os
# # import tabula
# def extract_pdf_tables(source_directory = '../data/pdfs', target_directory = '../data/pdf_tables'):
#     for filename in os.listdir(source_directory):
#         if filename.endswith('.pdf'):
#             pdf_path = os.path.join(source_directory, filename)
#             output_path = os.path.join(target_directory, f'{filename}_tables.csv')
            
#             # Extract tables using tabula
#             tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
            
#             if tables:
#                 # Concatenate all tables into a single DataFrame
#                 concatenated_tables = pd.concat(tables)
                
#                 # Save the concatenated table to a CSV file
#                 concatenated_tables.to_csv(output_path, index=False)
#                 print(f'Tables extracted from {filename} and saved as {output_path}')
#             else:
#                 print(f'No tables found in {filename}')