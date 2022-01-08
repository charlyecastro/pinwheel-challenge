import os
import re
import requests
from bs4 import BeautifulSoup
from lxml import etree
from colorama import init, Fore

BASE_URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"
BASE_SORT_QUERY = "?sortColumn=currentYearRevDate&indexOfFirstRow=0&criteria=formNumber&resultsPerPage=25"

def main():
    init(autoreset=True)

    # print(get_forms_info(["Form 11-C", "Form W-2 P"]))
    find_pdf("Form 707", 1935)
    # download_files("Form 707", 1935, 1937)

def is_input_acceptable(input: str):
    return False # Regex needed
    #@, /, &, (, ), *, hyphens, spaces, periods, and commas

# returns an array of dictionaries contianing info for each product provided
def get_forms_info(forms_list: list[str]):
    result = []
    for form in forms_list:
        info = get_form_info(form)
        result.append(info)
    return result

def get_form_info(form_name: str):
    if (not is_input_acceptable(form_name)):
        return

    reformated_form_name = form_name.replace(" ", "+")
    desc_query = BASE_URL + BASE_SORT_QUERY + "&isDescending=true&value=" + reformated_form_name
    asc_query = BASE_URL + BASE_SORT_QUERY + "&isDescending=false&value=" + reformated_form_name
    
    # Parse descending results
    desc_page = requests.get(desc_query)
    desc_soup = BeautifulSoup(desc_page.text, 'html.parser')

    # Grab the first desc row that exactly matches the given form_name
    matching_desc_row = desc_soup.find("a", text=form_name).parent.parent

    # Parse ascending results
    asc_page = requests.get(asc_query)
    asc_soup = BeautifulSoup(asc_page.text, 'html.parser')

    # Grab the first asc row that exactly matches the given form_name
    matching_asc_row = asc_soup.find("a", text=form_name).parent.parent
    
    # Grab data from ascending row and descending row
    form_number = matching_desc_row.find("td", class_="LeftCellSpacer").getText().strip()
    form_title = matching_desc_row.find("td", class_="MiddleCellSpacer").getText().strip()
    max_year = matching_desc_row.find("td", class_="EndCellSpacer").getText().strip()
    min_year = matching_asc_row.find("td", class_="EndCellSpacer").getText().strip()

    return {
        "form_number" : form_number, 
        "form_title" : form_title,
        "min_year" : int(min_year), 
        "max_year" : int(max_year) 
    }

def download_files(form_name: str, begin_year: int, end_year: int):
    if (not is_input_acceptable(form_name)):
        return

    for y in range(begin_year, end_year + 1):
        find_pdf(form_name, y)

def find_pdf(form_name: str, year: int):
    if (not is_input_acceptable(form_name)):
        print(Fore.RED + "Input '" + form_name + "' contains invalid characters")
        return
    # show 200 results per page
    # check if next page contains a link
    # make sure list is in ascending order
    reformated_form_name = form_name.replace(" ", "+")
    desc_query = BASE_URL + BASE_SORT_QUERY + "&isDescending=true&value=" + reformated_form_name
    
    # Parse descending results
    page = requests.get(desc_query)
    soup = BeautifulSoup(page.content, 'html.parser')

    dom = etree.HTML(str(soup))

    pdf_list = dom.xpath(f"//tr[td/a[text() = '{form_name}']  and td[@class='EndCellSpacer' and contains(text(),'{year}')]]/td/a/@href")

    # if pdf_list:
    #     return pdf_list[0]
    # return None
    pdf_link = pdf_list[0]
    print(pdf_list)
    download_pdf(form_name, year, pdf_link)

# Downloads a file 
def download_pdf(form_name: str, year: int, url: str):   
    folder = "./" + form_name
    file_name = form_name + " - " + str(year) + ".pdf"

    if not os.path.exists(folder):
        os.mkdir(folder)

    response = requests.get(url)
    file_path = os.path.join(folder,file_name)

    with open(file_path, 'wb') as f:
        f.write(response.content)
    
    print(Fore.GREEN + "Succefully Downloaded '" + file_name + "'")

if __name__ == "__main__":
    main()