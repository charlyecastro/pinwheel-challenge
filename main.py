import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"


def main():
    download_pdfs("test", 2010, 2020)

# returns an array of dictionaries contianing info for each product provided
def get_forms_info(forms_list: list):
    return []

def download_pdfs(form_name: str, begin: int, end: int):
    pdf_test = "https://www.irs.gov/pub/irs-prior/p1--2017.pdf"
    
    response = requests.get(pdf_test)
    file_path = "./" + form_name + " - " + str(begin) + ".pdf"

    os.mkdir("./test")
    # with open(file_path, 'wb') as f:
    #     f.write(response.content)
    
    print("Success")

if __name__ == "__main__":
    main()